import flask_login
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from .models import Scheduler
from home_assistant.appliances.models import Appliance
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
    appliances = request.form.getlist('appliances')
    scheduler = Scheduler(
        name=name,
        cron=cron,
    )
    for appliance in appliances:
        appliance_object = Appliance.query.get(appliance)
        scheduler.appliances.append(appliance_object)

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
    appliances = request.form.getlist('appliances')
    scheduler_id = request.form.get("scheduler_id")
    scheduler = Scheduler.query.get(scheduler_id)
    if scheduler:
        scheduler.name = name
        scheduler.cron = cron
        scheduler.appliances = []
        for appliance in appliances:
            appliance_object = Appliance.query.get(appliance)
            scheduler.appliances.append(appliance_object)
        db.session.commit()
        return redirect('/scheduler/all')

    return "No light found"


@scheduler.route("/scheduler/delete", methods=["POST"])
@login_required
def scheduler_put_update():
    scheduler_id = request.form.get('scheduler_id')
    scheduler = Scheduler.query.get(scheduler_id)
    db.session.delete(scheduler)
    db.session.commit()
    return redirect("/scheduler/all")