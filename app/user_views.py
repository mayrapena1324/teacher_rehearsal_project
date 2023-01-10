from flask_login import logout_user, current_user, login_required
from flask import render_template, url_for, redirect, flash, request
from flask import current_app as app
from .models import db, Rehearsal
from .forms import RehearsalForm
from datetime import datetime, date


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/all-rehearsals")
@login_required
def all_rehearsals():
    return render_template('user/all_rehearsals.html', current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal", methods=["GET", "POST"])
def rehearsal():
    if not current_user.is_authenticated:
        flash("You need to login or register to start rehearsing.")
        return redirect(url_for("login"))
    form = Rehearsal()
    if request.method == "POST":
        # The text box needs to display anything in the database for that lesson
        # create an edit functionality - Text editor will come up

        return redirect(request.url)
    return render_template("user/rehearsal.html", form=form, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/warm-up")
@login_required
def warm_up():
    return render_template("user/warm_up.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/rehearsal/music")
@login_required
def music():
    return render_template("user/music.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/rehearsal/goals")
@login_required
def goals():
    return render_template("user/goals.html", current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/rehearsal/create", methods=["GET", "POST"])
@login_required
def create():
    form = RehearsalForm()
    if request.method == "POST":
        req = request.form
        r_date = req.get("date")

        # Use strptime to convert the string to a datetime object
        date = datetime.strptime(r_date, '%Y-%m-%d').date()

        entry = Rehearsal(
            date=date
        )
        db.session.add(entry)
        db.session.commit()
        print("Success")
        return redirect(url_for('rehearsal'))
    return render_template("user/create.html", form=form)


# @app.route("/rehearsal/create/warm-up", methods=["GET", "POST"])
# def create_warmup():
#     form = RehearsalForm()
#     if request.method == "POST":
#         req = request.form
#
#
#         # formatted_date = date(rehearsal_date)
#         # entry = Rehearsal(
#         #     date=formatted_date
#         # )
#         # db.session.add(entry)
#         # db.session.commit()
#         return redirect(url_for('rehearsal'))
#
#     return render_template("user/create_warmup.html")


@app.route("/rehearsal/create/music")
def create_music():
    return render_template("user/create_music.html")


@app.route("/rehearsal/create/goals")
def create_goals():
    return render_template("user/create_goals.html")
