from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap


# configure flask
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'SECRET_APP_KEY'
Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/rehearsal", methods=["GET", "POST"])
def rehearsal():
    return render_template("rehearsal.html")

@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("faq.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
