from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from .auth import auth
from  flask_login import LoginManager
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    #create a flask app
    app = Flask(__name__)
    #create a bootstrap implementation/ receives a flask app
    bootstrap = Bootstrap(app)
    #encrypt data (cookie)
    app.config.from_object(Config)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return app

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)