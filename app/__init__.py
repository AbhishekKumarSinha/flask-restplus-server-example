# encoding: utf-8
"""
Example RESTful API Server.
"""
import logging
import os

from flask import Flask


CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
    'local': 'local_config.LocalConfig',
}

def create_app(flask_config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    app = Flask(__name__, **kwargs)

    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'production'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                "FLASK_CONFIG environment variable (\"%s\") and flask_config_name argument "
                "(\"%s\") are both set and are not the same." % (
                    env_flask_config_name,
                    flask_config_name
                )
            )
    app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])

    if app.debug:
        logging.getLogger('flask_oauthlib').setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)

        # We don't need default Flask's loggers when using invoke tasks as the
        # latter set up colorful loggers.
        for handler in app.logger.handlers:
            app.logger.removeHandler(handler)

    from . import extensions
    extensions.init_app(app)

    from . import modules
    modules.init_app(app)

    return app
