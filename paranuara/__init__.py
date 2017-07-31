import logging

from flask import Flask, redirect, session, url_for

def create_app(debug=False, testing=False, config_overrides=None):
    print (__name__)
    app = Flask(__name__)

    app.debug = debug
    app.testing = testing

    @app.route('/')
    def index():
        return redirect(url_for('crud.get_companies'))

    # Register the Phonebook CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud, url_prefix='/paranuara')


    # Add an error handler that reports exceptions to Stackdriver Error
    # Reporting. Note that this error handler is only used when debug
    # is False
    # [START setup_error_reporting]
    @app.errorhandler(500)
    def server_error(e):
        # client = error_reporting.Client(app.config['PROJECT_ID'])
        # client.report_exception(
        #     http_context=error_reporting.build_flask_context(request))
        return """
        An internal error occurred.
        """, 500
    # [END setup_error_reporting]

    return app


