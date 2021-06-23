from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
db = SQLAlchemy()
from home_assistant.schedulers.models import Scheduler

engine = create_engine('sqlite:///db.sqlite3')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    migrate = Migrate(app, db)
    db.init_app(app)
    migrate.init_app(app, db)

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
from home_assistant.service import set_gpio_appliances_from_scheduler, intialize_app_cron_jobs

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

intialize_app_cron_jobs()
