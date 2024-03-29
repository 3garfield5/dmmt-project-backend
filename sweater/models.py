from flask_login import UserMixin

from sweater import db, manager

#класс создания таблицы в БД
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)