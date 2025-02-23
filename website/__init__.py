from flask import Flask, render_template
from os import path
from flask_login import LoginManager



def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pewpewpew' #Change this before ever deploying if i need to

    from .views import views
    from .auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app