import asyncio
import os
import sys
import time
from multiprocessing import Process, Value

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

import constants

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    migrate = Migrate(app, db)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    return app


app = create_app()
from home_assistant.appliances.views import appliance as appliance_blueprint
from home_assistant.auth.views import auth as auth_blueprint
from home_assistant.categories.views import category as category_blueprint
from home_assistant.main.views import main as main_blueprint
from home_assistant.schedulers.views import scheduler as scheduler_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(appliance_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(scheduler_blueprint)
db.create_all(app=create_app())

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


from home_assistant.auth.models import User
from home_assistant.service import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


intialize_app_cron_jobs()


def record_loop(loop_on):
    """Send email to every user if temp is over * in an hour time span"""
    session = Session(engine)
    waiter = 0
    while True:
        if loop_on.value == True:
            current_temp = get_current_temperature()
            if constants.TARGET_TEMPERATURE in current_temp and waiter == 0:
                users = session.query(User).all()
                loop = asyncio.get_event_loop()
                tasks = []
                for user in users:
                    email_data = {
                        "subject": "Alarming Temperature in the room",
                        "to": user.email,
                        "body": f"Temperature is {current_temp} do something.",
                    }
                    tasks.append(
                        loop.create_task(send_async_email(email_data))
                    )
                loop.run_until_complete(asyncio.wait(tasks))
                loop.close()
                waiter = 3600  # an hour
        time.sleep(1)
        if waiter > 0:
            waiter -= 1
        print(waiter)
    session.close()


async def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(
        email_data["subject"],
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email_data["to"]],
    )
    msg.body = email_data["body"]
    with app.app_context():
        mail.send(msg)


if __name__ == "__main__":
    recording_on = Value("b", True)  # 'b' means byte
    p = Process(target=record_loop, args=(recording_on,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
