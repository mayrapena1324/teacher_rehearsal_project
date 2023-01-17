from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, flash, request, abort
from flask import current_app as app
from sqlalchemy import insert
from .models import db, Rehearsal, User
from .forms import RehearsalForm, OrderForm
import datetime as dt


@app.route("/all-rehearsals", methods=["GET", "POST"])
@login_required
def get_all_rehearsals():
    form = OrderForm()
    order_by = request.args.get("order_by")
    if not order_by:
        # Handle the case when the user does not select any option
        # redirect the user to a default ordering
        return redirect(url_for("get_all_rehearsals", order_by="desc"))
    elif order_by not in ["asc", "desc", "created"]:
        # Handle the case when the user is trying to manipulate the order_by parameter
        # return an error message
        flash("Invalid value for the order_by parameter")
        return redirect(url_for("get_all_rehearsals", order_by="desc"))
    else:

        if order_by == "desc":
            order_by_clause = Rehearsal.date.desc()
        elif order_by == "created":
            order_by_clause = Rehearsal.user_id.asc()
        else:
            order_by_clause = Rehearsal.date.asc()
        rehearsals = Rehearsal.query.filter_by(user_id=current_user.id).order_by(order_by_clause)
    # filter by distinct
    distinct_groups = db.session.query(Rehearsal.group).filter_by(user_id=current_user.id).distinct().all()
    return render_template('user/all_rehearsals.html', all_rehearsals=rehearsals, current_user=current_user,
                           logged_in=current_user.is_authenticated, distinct_groups=distinct_groups, form=form,
                           order_by=order_by)


@app.route("/rehearsal/create", methods=["GET", "POST"])
@login_required
def create():
    form = RehearsalForm()
    if form.validate_on_submit():
        print("Valid")
        user = User.query.filter_by(id=current_user.id).first()
        r_date = form.date.data
        group = form.group.data

        # Insert the row and get the cursor object
        result = db.session.execute(insert(Rehearsal).values(user_id=user.id, date=r_date, group=group))

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
    if requested_rehearsal.user_id != current_user.id:
        return abort(403)
    return render_template("user/rehearsal.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/edit_rehearsal/<rehearsal_id>', methods=['GET', 'POST'])
def edit_rehearsal(rehearsal_id):
    rehearsal_to_edit = Rehearsal.query.get(rehearsal_id)
    if rehearsal_to_edit.user_id != current_user.id:
        return abort(403)
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
        return redirect(url_for('warm_up', rehearsal_id=rehearsal_id))
    return render_template("user/edit_rehearsal.html", rehearsal_id=rehearsal_id, form=edit_form,
                           rehearsal=rehearsal_to_edit, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/warm-up", methods=["GET", "POST"])
def warm_up(rehearsal_id):
    form = RehearsalForm()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if requested_rehearsal.user_id != current_user.id:
        return abort(403)
    if form.validate_on_submit():
        return redirect(request.url)
    return render_template("user/warm_up.html", form=form, rehearsal=requested_rehearsal,
                           current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/music", methods=["GET", "POST"])
def music(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if requested_rehearsal.user_id != current_user.id:
        return abort(403)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/music.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/goals", methods=["GET", "POST"])
def goals(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if requested_rehearsal.user_id != current_user.id:
        return abort(403)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/goals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/fundamentals", methods=["GET", "POST"])
def fundamentals(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if requested_rehearsal.user_id != current_user.id:
        return abort(403)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/fundamentals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/delete/<int:rehearsal_id>", methods=["GET", "POST"])
def delete_rehearsal(rehearsal_id):
    rehearsal_to_delete = Rehearsal.query.get(rehearsal_id)
    if rehearsal_to_delete.user_id != current_user.id:
        return abort(403)
    db.session.delete(rehearsal_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_rehearsals'))
