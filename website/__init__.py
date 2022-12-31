from flask import Flask
from os import path
from flask_login import LoginManager

from .sqlHandeling import insertUser, getUserRecord_byID



def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pewpewpew'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app