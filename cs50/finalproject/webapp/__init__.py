# make website folder be python package
# use a package for larger application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message
import os


db = SQLAlchemy()
mail = Mail()

DB_NAME = "database.db"

def create_app():
    # configure the application
    app = Flask(__name__)
    # encrypt all sensitive information e.g. user's passwords
    app.config['SECRET_KEY'] = '8120ns'
    # store the database at the specified location (webapp folder) and connect the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # initalize the database
    db.init_app(app)

    from .views import views
    from .auth import auth
    # do the relative import to make sure run the model files to define the classes before initialize/create the database
    from .models import Users, Tracks

    # register the blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create the database
    create_database(app)

    
    # configure login process
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    # user_loader callback to reload the user object from the user ID stored in the session
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    # configure email setting
    app.config["MAIL_PASSWORD"] = "Hirtu8132"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True       
    app.config["MAIL_USERNAME"] = "samuelnhc@gmail.com"
    mail.init_app(app)

    return app

def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")