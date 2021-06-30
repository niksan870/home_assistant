from flask import Blueprint, render_template
from flask_login import login_required, current_user
from home_assistant.appliances.models import Appliance
from home_assistant.categories.models import Category
from home_assistant.schedulers.models import Scheduler
from home_assistant.service import get_current_temperature
from flask_mail import Mail, Message
from .. import mail


main = Blueprint('main', __name__)


@main.route('/')
def index():
    categories = Category.query.all()
    # current_temp = get_current_temperature()
    # if "29." in current_temp:
    #     msg = Message("Hello",
    #               sender="flask_home_assistant_idk@gmail.com",
    #               recipients=[current_user.email])
    #     msg.body = "The temp is over 29 celsius it may be kind of hot idk. Turn on the air conditioner."
    #     msg.html = "<b>The temp is over 29 celsius it may be kind of hot idk.</b>"
    #     mail.send(msg)
    return render_template('main/index.html', categories=categories, temperature=current_temp)


@main.route('/profile')
@login_required
def profile():
    appliances = Appliance.query.filter_by(user_id=current_user.id).all()
    schedulers = Scheduler.query.filter_by(user_id=current_user.id).all()
    return render_template('main/profile.html', name=current_user.name, num_of_appliances=len(appliances), num_of_schedulers=len(schedulers))
