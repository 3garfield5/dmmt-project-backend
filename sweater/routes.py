from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

from sweater import db, app
from sweater.models import Users

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
        # получаем данные из формы HTML

        rep_email = db.session.query(Users.id).filter(Users.email == email)

        if db.session.query(rep_email.exists()).scalar() == True: # проверяем повтор почты в БД, если есть, то выполняется условие

            user = Users.query.where(Users.email == email).first() # получаем значение пароля, где введенная почта = почте в БД
            if check_password_hash(user.password, password) == True: # так как мы хэшировали пароль, теперь проверяем введенный пароль, при помощи этой функции

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

