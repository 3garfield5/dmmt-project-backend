from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__) # приложение Flask
app.secret_key = 'secret key uauauauauaaaao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web-site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # база данных
manager = LoginManager(app) # менеджер для реализации входа в аккаунт

from sweater import models, routes