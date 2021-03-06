import flask_login
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from home_assistant.categories.models import Category
from home_assistant.service import set_gpio_appliances
from werkzeug.utils import redirect

from .. import db
from .models import Appliance

appliance = Blueprint("appliance", __name__)


@appliance.route("/appliance/all")
@login_required
def appliances():
    categories = Category.query.all()
    appliances = Appliance.query.filter_by(user_id=current_user.id).all()
    set_gpio_appliances(appliances)

    return render_template(
        "appliances/appliances.html",
        appliances=appliances,
        categories=categories,
    )


@appliance.route("/appliance/create")
@login_required
def appliance_get_create():
    categories = Category.query.all()
    return render_template(
        "appliances/appliance_create.html", categories=categories
    )


@appliance.route("/appliance", methods=["POST"])
@login_required
def appliance_post_create():
    name = request.form.get("name")
    pin_num = request.form.get("pin_num")
    category_id = request.form.get("category_id")
    state = request.form.get("state")
    running_state = request.form.get("running_state")

    appliance = Appliance(
        name=name,
        pin_num=pin_num,
        state=state,
        running_state=running_state,
        category_id=category_id,
        user_id=flask_login.current_user.id,
    )

    db.session.add(appliance)
    db.session.commit()
    return redirect("/appliance/all")


@appliance.route("/appliance/<int:id>", methods=["GET"])
@login_required
def appliance_get_update(id):
    if not id or id != 0:
        categories = Category.query.all()
        appliance = Appliance.query.get(id)
        if appliance:
            return render_template(
                "appliances/appliance_update.html",
                appliance=appliance,
                categories=categories,
            )

    return "No appliance found"


@appliance.route("/appliance/update", methods=["POST"])
@login_required
def appliance_post_update():
    name = request.form.get("name")
    state = request.form.get("state")
    pin_num = request.form.get("pin_num")
    category_id = request.form.get("category_id")
    appliance_id = request.form.get("appliance_id")
    running_state = request.form.get("running_state")
    if not appliance_id or appliance_id != 0:
        appliance = Appliance.query.get(appliance_id)
        if appliance and appliance.user_id == flask_login.current_user.id:
            appliance.name = name
            appliance.pin_num = pin_num
            appliance.category_id = category_id

            appliance.state = state
            appliance.previous_state = state
            appliance.running_state = running_state
            db.session.commit()
        return redirect("/appliance/all")

    return "No appliance found"


@appliance.route("/appliance/delete", methods=["POST"])
@login_required
def appliance_post_delete():
    appliance_id = request.form.get("appliance_id")
    appliance = Appliance.query.get(appliance_id)
    db.session.delete(appliance)
    db.session.commit()
    return redirect("/appliance/all")


@appliance.route("/appliance/switch", methods=["POST"])
@login_required
def appliance_post_switch():
    appliance_id = request.form.get("appliance_id")
    appliance = Appliance.query.get(appliance_id)
    if appliance.state == 0:
        appliance.state = 1
    else:
        appliance.state = 0
    db.session.commit()
    return redirect("/appliance/all")


@appliance.route("/appliance/run_initial", methods=["POST"])
@login_required
def appliance_post_run_initial():
    appliance_id = request.form.get("appliance_id")
    appliance = Appliance.query.get(appliance_id)
    appliance.previous_state = None
    db.session.commit()
    return redirect("/appliance/all")
