from flask import current_app as app
from flask import render_template, request


# authentication error
@app.errorhandler(403)
def forbidden(e):
    app.logger.error(f"Forbidden Access{e}, route: {request.url}")  # pass in the error itself and the error
    return render_template("public/error_handlers/403.html")
