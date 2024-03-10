from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) # приложение Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web-site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # база данных

from sweater import models, routes