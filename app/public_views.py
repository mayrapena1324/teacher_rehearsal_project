from flask import current_app as app
from flask_login import current_user
from flask import render_template


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("public/index.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("public/faq.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/pricing")
def pricing():
    return render_template("public/pricing.html", current_user=current_user, logged_in=current_user.is_authenticated)
