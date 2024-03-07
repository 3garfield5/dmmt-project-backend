from flask import Flask, redirect, render_template, request
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) # приложение Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web-site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # база данных


#класс создания таблицы в БД
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


#роут на главную страницу
@app.route('/', methods=['POST', 'GET'])
def index():
    # try:
    #    db.session.query(Users).delete()
    #    db.session.commit()
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
        email = request.form['email']
        password = request.form['password']
        # получаем данные из формы HTML

        rep_email = db.session.query(Users.id).filter(Users.email == email)
        if db.session.query(rep_email.exists()).scalar() == False: #проверяем есть ли такая почта в БД

            password = generate_password_hash(password) # хэшируем пароль для безопасности
            user = Users(name=name, email=email, password=password)

            try:
                db.session.add(user) # добавляем данные из формы в БД
                db.session.commit() # сохраняем данные в БД
                return 'Успешно'
            except:
                return 'При добавлении данных произошла ошибка!'
        else:
            return 'Почта уже зарегистрирована'

    return render_template('registration.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        rep_email = db.session.query(Users.id).filter(Users.email == email)

        if db.session.query(rep_email.exists()).scalar() == True:

            user = Users.query.where(Users.email == email).first()
            if check_password_hash(user.password, password) == True:

                return 'успешно'

            else:
                return 'Пароль не верный'

        else:
            return 'Такой почты не существует!'
    return render_template('login.html')

#роут на страницу личного кабинета
@app.route('/per_acc', methods=['GET'])
def acc():
    user = Users.query.all()
    return render_template('per_acc.html', user=user)


#запуск сервера с возможностью дебага в режиме реального времени
if __name__ == '__main__':
    app.run(debug=True)