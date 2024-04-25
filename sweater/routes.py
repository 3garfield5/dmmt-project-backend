from flask import redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
import random


from sweater.dw_project import metro_list_1, metro_list_2, metro_list_3, metro_list
from sweater import db, app
from sweater.models import Users, BotReq
#роут на главную страницу
@app.route('/', methods=['POST', 'GET'])
def index():
    # try:
    #    db.session.query(Users).delete()
    #    db.session.commit()
    # except:
    #     db.session.rollback()
    name = request.form.get('name')
    tg = request.form.get('tg')

    if request.method == 'POST':
        try:
            bot = BotReq(name=name, tg=tg)
            db.session.add(bot)
            db.session.commit()  # добавляем данные в бд
        except:
            flash('Error, this nickname is zanyat')
        return render_template('index.html')

    metro = random.choice(metro_list)
    return render_template('index.html', metro=metro, metro_list_1=metro_list_1, metro_list_2=metro_list_2, metro_list_3=metro_list_3)

#роут на страницу регистрации
@app.route('/registration', methods=['POST','GET'])
def registration():

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    # получаем данные из формы HTML

    if request.method == 'POST':
        if not (name or email or password):
            flash('Please, fill all fields!') # проверяем заполнены ли все поля
        else:
            rep_email = db.session.query(Users.id).filter(Users.email == email)
            if db.session.query(rep_email.exists()).scalar() == False: #проверяем есть ли такая почта в БД

                hash_pwr = generate_password_hash(password) # хэшируем пароль
                new_user = Users(name=name, email=email, password=hash_pwr)
                db.session.add(new_user)
                db.session.commit() # добавляем данные в бд

                return redirect('login')
            else:
                flash('An account with such an email has already been registered')
    else:
        flash('Please fill name, email and password fields')

    return render_template('regist.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = Users.query.filter_by(email=email).first()

        rep_email = db.session.query(Users.id).filter(Users.email == email)
        if db.session.query(rep_email.exists()).scalar() == True: # проверяем повтор почты в БД, если есть, то выполняется условие

            if user and check_password_hash(user.password, password): # проверяем правильность пароля
                login_user(user) # выполняем вход в аккаунт

                return redirect('per_acc')
            else:
                flash('Login or password is not correct')
        else:
            flash('You are not in system ')
    else:
        flash('Please fill login or password fields')

    return render_template('login1.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user() # функция выхода человека из аккаунта
    return redirect(url_for('index'))

#роут на страницу личного кабинета
@app.route('/per_acc', methods=['GET'])
@login_required
def acc():
    return render_template('per_acc.html')

@app.route('/collection')
def collection():
    return 'Collection'

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
