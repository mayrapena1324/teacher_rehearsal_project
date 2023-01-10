from flask_login import logout_user, current_user, login_required
from flask import render_template, url_for, redirect, flash, request
from flask import current_app as app
from sqlalchemy import insert

from .models import db, Rehearsal
from .forms import RehearsalForm
from datetime import datetime, date


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/all-rehearsals")
@login_required
def get_all_rehearsals():
    rehearsals = Rehearsal.query.all()
    return render_template('user/all_rehearsals.html', all_rehearsals=rehearsals, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/create", methods=["GET", "POST"])
@login_required
def create():
    form = RehearsalForm()
    if request.method == "POST":
        import datetime as dt

        req = request.form
        r_date = req.get("date")

        # Use the datetime module to parse the date string
        date_time = dt.datetime.strptime(r_date, '%Y-%m-%d')

        # Convert the datetime object to a date object
        date = date_time.date()

        # Insert the row and get the cursor object
        result = db.session.execute(insert(Rehearsal).values(date=date))

        # Get the id of the inserted row using the lastrowid attribute
        entry_id = result.lastrowid

        # Commit the transaction
        db.session.commit()

        return redirect(url_for('rehearsal', rehearsal_id=entry_id))
    return render_template("user/create.html", form=form)


@app.route("/rehearsal/<rehearsal_id>", methods=["GET", "POST"])
def rehearsal(rehearsal_id):
    if not current_user.is_authenticated:
        flash("You need to login or register to start rehearsing.")
        return redirect(url_for("login"))
    form = Rehearsal()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        # The text box needs to display anything in the database for that lesson
        # create an edit functionality - Text editor will come up

        return redirect(request.url)
    return render_template("user/rehearsal.html", rehearsal=requested_rehearsal, form=form, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/warm-up", methods=["GET", "POST"])
def warm_up(rehearsal_id):
    form = Rehearsal()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/warm_up.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/music", methods=["GET", "POST"])
def music(rehearsal_id):
    form = Rehearsal()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/music.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/goals", methods=["GET", "POST"])
def goals(rehearsal_id):
    form = Rehearsal()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/goals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/fundamentals", methods=["GET", "POST"])
def fundamentals(rehearsal_id):
    form = Rehearsal()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/fundamentals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/delete/<int:rehearsal_id>")
def delete_post(rehearsal_id):
    post_to_delete = Rehearsal.query.get(rehearsal_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_rehearsals'))
