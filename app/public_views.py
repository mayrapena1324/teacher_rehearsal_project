from flask import current_app as app, abort
from flask_login import current_user
from flask import render_template
from .models import Rehearsal

SAMPLE = 22


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("public/index.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("public/faq.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/pricing")
def pricing():
    return render_template("public/pricing.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/sample-rehearsal")
def sample_rehearsal():
    return render_template("public/sample_rehearsal.html", rehearsal_id=SAMPLE)


@app.route("/sample_rehearsal/warm-up", methods=["GET", "POST"])
def sample_warm_up():
    requested_rehearsal = Rehearsal.query.get(SAMPLE)
    return render_template("public/sample_warm_up.html", rehearsal=requested_rehearsal,
                           current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/sample_rehearsal/fundamentals", methods=["GET", "POST"])
def sample_fundamentals():
    requested_rehearsal = Rehearsal.query.get(SAMPLE)
    return render_template("public/sample_fundamentals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/sample_rehearsal/music", methods=["GET", "POST"])
def sample_music():
    requested_rehearsal = Rehearsal.query.get(SAMPLE)
    return render_template("public/sample_music.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/sample_rehearsal/goals", methods=["GET", "POST"])
def sample_goals():
    requested_rehearsal = Rehearsal.query.get(SAMPLE)
    return render_template("public/sample_goals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)

