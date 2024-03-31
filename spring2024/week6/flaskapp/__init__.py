from flask import Flask 
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '21k3n42kjnknj21k34jnkj'
app.config['MONGODB_SETTINGS'] = {
    'db': 'cmsc388j_db',
    'host': 'mongodb+srv://aakashpatel0377:mongoDBAakashMM@cluster0.tuubvqi.mongodb.net/cmsc388j_db?retryWrites=true&w=majority&appName=Cluster0'
}

db = MongoEngine(app)
login_manager = LoginManager(app)
# if the user is not logged in for a route that requires it, redirect to login_route
login_manager.login_view = 'login_route'
bcrypt = Bcrypt(app)