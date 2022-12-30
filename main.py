from flask import Flask, render_template, redirect, url_for, request

# configure flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_APP_KEY'


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)