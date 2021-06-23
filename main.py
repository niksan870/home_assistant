from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .appliances.models import Appliance
from .categories.models import Category
from .schedulers.models import Scheduler
from home_assistant.service import get_current_temperature

main = Blueprint('main', __name__)


@main.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories, temperature=get_current_temperature())


@main.route('/profile')
@login_required
def profile():
    appliances = Appliance.query.filter_by(user_id=current_user.id).all()
    schedulers = Scheduler.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', name=current_user.name, num_of_appliances=len(appliances), num_of_schedulers=len(schedulers))
