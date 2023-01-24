import weasyprint
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, flash, request, abort, make_response, send_file
from flask import current_app as app
from sqlalchemy import insert
from .models import db, Rehearsal, User
from .forms import RehearsalForm, OrderForm
import datetime as dt
from functools import wraps


def check_rehearsal_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        requested_rehearsal = Rehearsal.query.get(kwargs["rehearsal_id"])
        if requested_rehearsal.user_id != current_user.id:
            abort(403)
        return func(*args, **kwargs)

    return wrapper



@app.route("/generate-rehearsal/<int:rehearsal_id>")
def generate_rehearsal(rehearsal_id):
    # Get the rehearsal from the database
    rehearsal = Rehearsal.query.get(rehearsal_id)

    # Render the template to get the HTML content
    html_content = render_template("user/pdf/rehearsal_pdf.html", rehearsal=rehearsal)

    # Create the PDF
    pdf_content = weasyprint.HTML(string=html_content).write_pdf()

    # Create the response object with the PDF content
    response = make_response(pdf_content)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={rehearsal.group}-rehearsal-{rehearsal.date}.pdf"

    return response


@app.route("/all-rehearsals", methods=["GET", "POST"])
@login_required
def get_all_rehearsals():
    # Check date
    date_check = dt.datetime.today().date()
    today = date_check.strftime("%a %d %b, %Y")

    form = OrderForm()
    order_by = request.args.get("order_by")
    if not order_by:
        # Handle the case when the user does not select any option
        # redirect the user to a default ordering
        return redirect(url_for("get_all_rehearsals", order_by="desc"))
    elif order_by not in ["asc", "desc"]:
        # Handle the case when the user is trying to manipulate the order_by parameter
        # return an error message
        flash("Invalid value for the order_by parameter")
        return redirect(url_for("get_all_rehearsals", order_by="desc"))
    else:

        if order_by == "desc":
            order_by_clause = Rehearsal.date.desc()
        else:
            order_by_clause = Rehearsal.date.asc()
        rehearsals = Rehearsal.query.filter_by(user_id=current_user.id)
        if order_by == "desc":
            rehearsals = rehearsals.order_by(Rehearsal.date.desc())
        elif order_by == "created":
            rehearsals = rehearsals.order_by(Rehearsal.user_id.asc())
        else:
            rehearsals = rehearsals.order_by(Rehearsal.date.asc())

    # filter by distinct
    distinct_groups = db.session.query(Rehearsal.group).filter_by(user_id=current_user.id).distinct().all()

    return render_template('user/all_rehearsals.html', all_rehearsals=rehearsals, current_user=current_user,
                           logged_in=current_user.is_authenticated, distinct_groups=distinct_groups, form=form,
                           order_by=order_by, today=today, date_check=date_check)


@app.route("/rehearsal/create", methods=["GET", "POST"])
@login_required
def create():
    form = RehearsalForm()
    if form.validate_on_submit():
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
@check_rehearsal_user
def rehearsal(rehearsal_id):
    if not current_user.is_authenticated:
        flash("You need to login or register to start rehearsing.")
        return redirect(url_for("login"))

    requested_rehearsal = Rehearsal.query.get(rehearsal_id)

    return render_template("user/rehearsal.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/edit_rehearsal/<rehearsal_id>', methods=['GET', 'POST'])
@check_rehearsal_user
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
        return redirect(url_for('warm_up', rehearsal_id=rehearsal_id))
    return render_template("user/edit_rehearsal.html", rehearsal_id=rehearsal_id, form=edit_form,
                           rehearsal=rehearsal_to_edit, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/warm-up", methods=["GET", "POST"])
@check_rehearsal_user
def warm_up(rehearsal_id):
    form = RehearsalForm()
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)

    if form.validate_on_submit():
        return redirect(request.url)
    return render_template("user/warm_up.html", form=form, rehearsal=requested_rehearsal,
                           current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/music", methods=["GET", "POST"])
@check_rehearsal_user
def music(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)

    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/music.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/goals", methods=["GET", "POST"])
@check_rehearsal_user
def goals(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)
    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/goals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/rehearsal/<rehearsal_id>/fundamentals", methods=["GET", "POST"])
@check_rehearsal_user
def fundamentals(rehearsal_id):
    requested_rehearsal = Rehearsal.query.get(rehearsal_id)

    if request.method == "POST":
        return redirect(request.url)
    return render_template("user/fundamentals.html", rehearsal=requested_rehearsal, current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/delete/<int:rehearsal_id>", methods=["GET", "POST"])
@check_rehearsal_user
def delete_rehearsal(rehearsal_id):
    rehearsal_to_delete = Rehearsal.query.get(rehearsal_id)

    db.session.delete(rehearsal_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_rehearsals'))
