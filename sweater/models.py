from flask_login import UserMixin

from sweater import db, manager

#класс создания таблицы в БД
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class BotReq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)
    tg = db.Column(db.String(100), nullable=True)

class BagBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=False)
    tg = db.Column(db.String(100), nullable=True, unique=True)
    bag = db.Column(db.String(1000), nullable=True)

@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)