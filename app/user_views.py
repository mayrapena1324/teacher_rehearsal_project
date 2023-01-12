from flask_login import logout_user, current_user, login_required
from flask import render_template, url_for, redirect, flash, request
from flask import current_app as app
from sqlalchemy import insert
from .models import db, Rehearsal
from .forms import RehearsalForm
import datetime as dt


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
        req = request.form
        r_date = req.get("date")
        group = req.get("group")
        # Use the datetime module to parse the date string
        date_time = dt.datetime.strptime(r_date, '%Y-%m-%d')

        # Convert the datetime object to a date object
        date = date_time.date()

        # Insert the row and get the cursor object
        result = db.session.execute(insert(Rehearsal).values(date=date, group=group))

        # Get the id of the inserted row using the lastrowid attribute
        entry_id = result.lastrowid

        # Commit the transaction
        db.session.commit()

        return redirect(url_for('rehearsal', rehearsal_id=entry_id))
    return render_template("user/create.html", form=form, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>", methods=["GET", "POST"])
def rehearsal(rehearsal_id):
    if not current_user.is_authenticated:
        flash("You need to login or register to start rehearsing.")
        return redirect(url_for("login"))

    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    return render_template("user/rehearsal.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/edit_rehearsal/<rehearsal_id>', methods=['GET', 'POST'])
def edit_rehearsal(rehearsal_id):
    rehearsal_to_edit = Rehearsal.query.get(rehearsal_id)
    edit_form = RehearsalForm(
        date=rehearsal_to_edit.date,
        group=rehearsal_to_edit.group,
        warm_up=rehearsal_to_edit.warm_up,
        fundamentals=rehearsal_to_edit.fundamentals,
        music=rehearsal_to_edit.music,
        goals=rehearsal_to_edit.goals,
    )
    if request.method == 'POST':
        if edit_form.cancel.data:  # if cancel button is clicked, the form.cancel.data will be True
            return redirect(url_for('rehearsal', rehearsal_id=rehearsal_id))
    # Retrieve the text from the database

    if request.method == "POST":
        rehearsal_to_edit.date = edit_form.date.data
        rehearsal_to_edit.group = edit_form.group.data
        rehearsal_to_edit.warm_up = edit_form.warm_up.data
        rehearsal_to_edit.fundamentals = edit_form.fundamentals.data
        rehearsal_to_edit.music = edit_form.music.data
        rehearsal_to_edit.goals = edit_form.goals.data
        db.session.commit()
        return redirect(url_for('rehearsal', rehearsal_id=rehearsal_id))
    return render_template("user/edit_rehearsal.html", rehearsal_id=rehearsal_id, form=edit_form,
                           rehearsal=rehearsal_to_edit, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/warm-up", methods=["GET", "POST"])
def warm_up(rehearsal_id):
    form = RehearsalForm()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if form.validate_on_submit():
        return redirect(request.url)
    return render_template("user/warm_up.html", form=form, rehearsal=requested_rehearsal,
                           current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/music", methods=["GET", "POST"])
def music(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/music.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/goals", methods=["GET", "POST"])
def goals(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/goals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/fundamentals", methods=["GET", "POST"])
def fundamentals(rehearsal_id):
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
