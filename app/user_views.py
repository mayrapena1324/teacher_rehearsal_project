from flask_login import logout_user, current_user
from app import app
from flask import render_template, url_for, redirect, flash


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/rehearsal", methods=["GET", "POST"])
def rehearsal():
    if not current_user.is_authenticated:
        flash("You need to login or register to start rehearsing.")
        return redirect(url_for("login"))
    return render_template("rehearsal.html", current_user=current_user, logged_in=current_user.is_authenticated)