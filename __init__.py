from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from werkzeug.utils import redirect

from apscheduler.schedulers.background import BackgroundScheduler
db = SQLAlchemy()
from home_assistant.schedulers.models import Scheduler

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'niksan870@gmail.com'
    app.config['MAIL_PASSWORD'] = 'hlqnbtacqusvztlb'
    app.config['MAIL_USE_TLS'] = True

    migrate = Migrate(app, db)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    return app


app = create_app()
from .auth.views import auth as auth_blueprint
from .main.views import main as main_blueprint
from .appliances.views import appliance as appliance_blueprint
from .categories.views import category as category_blueprint
from .schedulers.views import scheduler as scheduler_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(appliance_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(scheduler_blueprint)
db.create_all(app=create_app())

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from .auth.models import User
from home_assistant.service import *


@app.route("/test_emailing")
def test_emailing():
    # Set up mailing
    send_email_if_room_temp_is_high()
    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

intialize_app_cron_jobs()
