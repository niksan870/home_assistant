import flask_login
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from .models import Scheduler
from home_assistant.appliances.models import Appliance
from home_assistant.service import *
from .. import db

scheduler = Blueprint('scheduler', __name__)

@scheduler.route('/scheduler/all')
@login_required
def schedulers():
    schedulers = Scheduler.query.all()
    return render_template('schedulers/schedulers.html', schedulers=schedulers)


@scheduler.route('/scheduler/create')
@login_required
def scheduler_get_create():
    appliances = Appliance.query.all()
    return render_template('schedulers/scheduler_create.html', appliances=appliances)


@scheduler.route('/scheduler', methods=['POST'])
@login_required
def scheduler_post_create():
    name = request.form.get('name')
    cron = request.form.get('cron')
    state = request.form.get('state')
    appliances = request.form.getlist('appliances')
    appliance_state = request.form.get('appliance_state')
    scheduler = Scheduler(
        name=name,
        cron=cron,
        appliances=Appliance.query.filter(Appliance.id.in_(appliances)).all(),
        appliance_state=appliance_state,
        state=state,
        user_id=flask_login.current_user.id,
    )
    if int(state) > 0:
        add_scheduler(scheduler)
    
    db.session.add(scheduler)
    db.session.commit()
    return redirect('/scheduler/all')

@scheduler.route('/scheduler/update/<int:id>', methods=["GET"])
@login_required
def scheduler_get_update(id):
    if not id or id != 0:
        appliances = Appliance.query.all()
        scheduler = Scheduler.query.get(id)
        if scheduler:
            return render_template('schedulers/scheduler_update.html', scheduler=scheduler, appliances=appliances)

    return "No light found"

@scheduler.route('/scheduler/<int:id>', methods=["GET"])
@login_required
def scheduler_get_view(id):
    if not id or id != 0:
        scheduler = Scheduler.query.get(id)
        if scheduler:
            return render_template('schedulers/scheduler_view.html', scheduler=scheduler)

    return "No light found"

@scheduler.route('/scheduler/update', methods=['POST'])
@login_required
def scheduler_post_update():
    name = request.form.get('name')
    cron = request.form.get('cron')
    state = request.form.get('state')
    appliances = request.form.getlist('appliances')
    scheduler_id = request.form.get("scheduler_id")
    appliance_state = request.form.get('appliance_state')
    scheduler = Scheduler.query.get(scheduler_id)
    if scheduler:
        prev_state = scheduler.state
        scheduler.name = name
        scheduler.cron = cron
        scheduler.state = state
        scheduler.appliances = Appliance.query.filter(Appliance.id.in_(appliances)).all()

        # if int(state) != prev_state:
        if int(state) == 0:
            set_gpio_appliances(scheduler.appliances)
            remove_scheduler(scheduler)
        else:
            add_scheduler(scheduler)

        db.session.commit()
        return redirect('/scheduler/all')

    return "No light found"


@scheduler.route("/scheduler/delete", methods=["POST"])
@login_required
def scheduler_put_delete():
    scheduler_id = request.form.get('scheduler_id')
    scheduler = Scheduler.query.get(scheduler_id)
    db.session.delete(scheduler)
    db.session.commit()
    return redirect("/scheduler/all")


@scheduler.route("/scheduler/switch", methods=["POST"])
@login_required
def scheduler_put_update():
    scheduler_id = request.form.get('scheduler_id')
    scheduler = Scheduler.query.get(scheduler_id)
    if scheduler.state == 0:
        add_scheduler(scheduler)
        scheduler.state = 1
    else:
        set_gpio_appliances(scheduler.appliances)
        remove_scheduler(scheduler)
        scheduler.state = 0
    db.session.commit()
    return redirect("/scheduler/all")