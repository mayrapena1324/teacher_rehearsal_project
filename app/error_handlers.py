from flask import current_app as app
from flask import render_template, request


def email_admin(message, error, url):
    pass


@app.errorhandler(404)
def not_found(e):
    return render_template("public/error_handlers/404.html")


@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server Error{e}, route: {request.url}")  # pass in the error itself and the error
    return render_template("public/error_handlers/500.html")


# authentication error
@app.errorhandler(403)
def forbidden(e):
    app.logger.error(f"Forbidden Access{e}, route: {request.url}")  # pass in the error itself and the error

    # email_admin(message="Server error", error=e, url=request.url)
    return render_template("public/error_handlers/403.html")
