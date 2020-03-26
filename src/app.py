from __future__ import absolute_import, unicode_literals
from flask import Flask
import os
import logging.config
import mongoengine
from flask_swagger_ui import get_swaggerui_blueprint


application = Flask(os.environ.get("APPLICATION_NAME"))
SETTINGS_FILE = os.environ.get("SETTINGS_FILE", "settings.local_settings")

application.config.from_object(SETTINGS_FILE)

with application.app_context():
    # this loads all the views with the app context
    # this is also helpful when the views import other
    # modules, this will load everything under the application
    # context and then one can use the current_app configuration
    # parameters
    from apis.urls import all_urls
    from scripts import ALL_CLI_COMMANDS

    for cli_name, cli_command in ALL_CLI_COMMANDS.items():
        application.cli.add_command(cli_command, name=cli_name)


# Adding all the url rules in the api application
for url, view, methods, _ in all_urls:
    application.add_url_rule(url, view_func=view, methods=methods)


logging.config.dictConfig(application.config["LOGGING"])

mongoengine.connect(
    alias='default',
    db=application.config['MONGO_SETTINGS']['DB_NAME'],
    host=application.config['MONGO_SETTINGS']['DB_HOST'],
    port=application.config['MONGO_SETTINGS']['DB_PORT'],
    username=application.config['MONGO_SETTINGS']['DB_USERNAME'],
    password=application.config['MONGO_SETTINGS']['DB_PASSWORD'],
)



@application.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Spotmentor"
    }
)
application.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

