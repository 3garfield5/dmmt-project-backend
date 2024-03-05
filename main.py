from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask, redirect, render_template, request,  jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

import base64
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web-site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return '<Users %r>' % self.id


app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "djfyt75"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

# @app.route("/login", methods=["POST"])
# def login():
#     response = jsonify({"msg": "login successful"})
#     access_token = create_access_token(identity="example_user")
#     set_access_cookies(response, access_token)
#     return response

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")

#роут на главную страницу
@app.route('/', methods=['POST', 'GET'])
def index():
    # try:
    #     db.session.query(Users).delete()
    #     db.session.commit()
    # except:
    #     db.session.rollback()
    if request.method == 'POST':
        return redirect('/registration')
    return render_template('index.html')

#роут на страницу регистрации
@app.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        email = request.form['email']
        password = request.form['password']
        password_rep = request.form['password_rep']

        rep_email = db.session.query(Users.id).filter(Users.email == email)
        if password == password_rep:
            if db.session.query(rep_email.exists()).scalar() == False:

                user = Users(name=name, surname=surname, patronymic=patronymic, email=email, password=password)

                try:
                    db.session.add(user)
                    db.session.commit()
                    return redirect('/login')
                except:
                    return 'При добавлении данных произошла ошибка!'
            else:
                return 'Почта уже зарегистрирована'
        else:
            return 'Вы написали разные пароли!'

    return render_template('registration.html')

#роут на страницу личного кабинета
@app.route('/per_acc', methods=['GET'])
def acc():
    return render_template('per_acc.html')





#запуск сервера с возможностью дебага в режиме реального времени
if __name__ == '__main__':
    app.run(debug=True)