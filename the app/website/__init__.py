from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
import pymongo
from flask_login.login_manager import LoginManager

def create_app():
    app= Flask(__name__)
    
    app.config['SECRET_KEY'] = 'kdshn'
    
    cluster = MongoClient("mongodb+srv://iamnivedhav:N1vedha@cluster0.hfklgll.mongodb.net/?retryWrites=true&w=majority",serverSelectionTimeoutMS=5000)
    db= cluster["myapp"]
    products = db["products"]
    users= db['users']

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.static_folder = 'static'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        id= int(id)
        return users.find_one({'user_id':id})

    return app