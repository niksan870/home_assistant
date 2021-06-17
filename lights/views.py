import flask_login
from flask import Blueprint, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect

from .models import Light
from .. import db

light = Blueprint('light', __name__)

@light.route('/lights')
@login_required
def lights():
    return render_template('lights.html', lights=Light.query.all())


@light.route('/lights/create')
@login_required
def lights_get_create():
    return render_template('lights_create.html')


@light.route('/lights', methods=['POST'])
@login_required
def lights_post_create():
    name = request.form.get('name')
    status = request.form.get('status')
    description = request.form.get('description')

    light = Light(
        name=name,
        description=description,
        user_id=flask_login.current_user.id,
        status=status
    )
    db.session.add(light)
    db.session.commit()
    return redirect('/lights')


@light.route('/lights/<int:id>', methods=["GET"])
@login_required
def lights_get_update(id):
    if not id or id != 0:
        light = Light.query.get(id)
        if light:
            return render_template('lights_update.html', light=light)

    return "No light found"


@light.route('/lights/update', methods=['POST'])
@login_required
def lights_post_update():
    name = request.form.get('name')
    status = request.form.get('status')
    light_id = request.form.get('light_id')
    description = request.form.get('description')
    if not light_id or light_id != 0:
        light = Light.query.get(light_id)
        if light and light.user_id == flask_login.current_user.id:
            light.name = name
            light.status = status
            light.description = description
            db.session.commit()
        return redirect('/lights')

    return "No light found"


@light.route("/lights/delete", methods=["POST"])
@login_required
def lights_put_update():
    light_id = request.form.get('light_id')
    light = Light.query.get(light_id)
    db.session.delete(light)
    db.session.commit()
    return redirect("/lights")
