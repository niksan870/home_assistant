from flask import Blueprint, render_template
from flask_login import current_user, login_required
from home_assistant.appliances.models import Appliance
from home_assistant.categories.models import Category
from home_assistant.schedulers.models import Scheduler
from home_assistant.service import get_current_temperature

main = Blueprint("main", __name__)


@main.route("/")
def index():
    categories = Category.query.all()
    current_temp = get_current_temperature()
    return render_template(
        "main/index.html", categories=categories, temperature=current_temp
    )


@main.route("/profile")
@login_required
def profile():
    appliances = Appliance.query.filter_by(user_id=current_user.id).all()
    schedulers = Scheduler.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "main/profile.html",
        name=current_user.name,
        num_of_appliances=len(appliances),
        num_of_schedulers=len(schedulers),
    )
