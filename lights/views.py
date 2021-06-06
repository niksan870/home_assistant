from flask import Blueprint, render_template
from flask_login import login_required

from .models import Light

light = Blueprint('light', __name__)


@light.route('/lights')
@login_required
def lights():
    lights = Light.query.all()
    return render_template('lights.html', lights=lights)
