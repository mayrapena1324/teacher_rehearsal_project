from flask_login import logout_user, current_user
from flask import render_template, url_for, redirect, flash, request
from flask import current_app as app
from .models import db, Rehearsal


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
