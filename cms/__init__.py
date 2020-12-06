from flask import Flask
from cms.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    '''
    Initializing various modules in the app

    :param config_class:
    :return: flask app
    '''
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from cms.user.routes import user
    from cms.posts.routes import posts
    from cms.main.routes import main
    from cms.errors.handlers import error

    app.register_blueprint(user)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(error)

    return app
