from flask import Blueprint, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect

from .. import db
from .models import Category

category = Blueprint("category", __name__)


@category.route("/category/all")
@login_required
def categories():
    categories = Category.query.all()
    return render_template("categories/categories.html", categories=categories)


@category.route("/category/create")
@login_required
def category_get_create():
    return render_template("categories/category_create.html")


@category.route("/category", methods=["POST"])
@login_required
def category_post_create():
    name = request.form.get("name")
    description = request.form.get("description")
    image = request.form.get("image")
    if not image:
        image = "https://blackmantkd.com/wp-content/uploads/2017/04/default-image.jpg"
    category = Category(
        name=name,
        description=description,
        image=image,
    )
    db.session.add(category)
    db.session.commit()
    return redirect("/category/all")


@category.route("/category/update/<int:id>", methods=["GET"])
@login_required
def category_get_update(id):
    if not id or id != 0:
        category = Category.query.get(id)
        if category:
            return render_template(
                "categories/category_update.html", category=category
            )

    return "No light found"


@category.route("/category/<int:id>", methods=["GET"])
@login_required
def category_get_view(id):
    if not id or id != 0:
        category = Category.query.get(id)
        if category:
            return render_template(
                "categories/category_view.html", category=category
            )

    return "No light found"


@category.route("/category/update", methods=["POST"])
@login_required
def category_post_update():
    name = request.form.get("name")
    image = request.form.get("image")
    description = request.form.get("description")
    category_id = request.form.get("category_id")
    if not category_id or category_id != 0:
        category = Category.query.get(category_id)
        if category:
            category.name = name
            category.image = image
            category.description = description
            db.session.commit()
        return redirect("/category/all")

    return "No light found"


@category.route("/category/delete", methods=["POST"])
@login_required
def category_put_update():
    category_id = request.form.get("category_id")
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect("/category/all")
