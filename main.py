from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

#функция создания базы данных
def get_db_connection():
    conn = sqlite3.connect('personal_account.db')
    conn.row_factory = sqlite3.Row
    return conn

#функция инициализации базы данных
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS personal_account (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, surname TEXT NOT NULL, patronymic TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)')
    conn.close()

#функция закрытия базы данных
def close_db_connection(conn):
    conn.close()

#функция очищения базы данных
def delete():
    conn = get_db_connection()
    conn.execute('DELETE from personal_account')
    conn.commit()
    conn.close()

#создание базы данных
@app.before_request
def before_first_request():
    init_db()

#роут на главную страницу
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect('/registration')
    return render_template('index.html')

#роут на страницу регистрации
@app.route('/registration', methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        email = request.form['email']
        password = request.form['password']

        #вывожу данные почты из базы данных в лист питона
        conn = get_db_connection()
        email_list = []
        for el in conn.execute('SELECT email FROM personal_account').fetchall():
            email_list.append(tuple(el))

        #проверяю есть ли такая почта в нашей базе данных
        flag = True
        for i in range(len(email_list)):
            if email != email_list[i][0]:
                flag = True
            else:
                flag = False

        #если флаг = правда, значит такой почты нет и человек может зарегистрироваться, если флаг = ложь,
        #то появляется сообщение о том, что пользователь с такой почтой уже зарегистрирован
        if flag == True:
            try:
                conn.execute('INSERT INTO personal_account (name, surname, patronymic, email, password) VALUES (?, ?, ?, ?, ?)', (name, surname, patronymic, email, password))
                conn.commit()
                conn.close()
                return redirect('/per_acc')
            except:
                return 'Из-за непредвиденных проблем произошла ошибка! Попробуйте еще раз!'
        else:
            return 'Пользователь с такой почтой уже зарегистрирован!'

    return render_template('registration.html')

#роут на страницу "о нас"
@app.route('/boute')
def aboute():
    return render_template('boute.html')

#роут на страницу личного кабинета
@app.route('/per_acc', methods=['GET'])
def acc():
    conn = get_db_connection()
    personal_account = conn.execute('SELECT * from personal_account').fetchall()
    conn.close()
    return render_template('per_acc.html', personal_account=personal_account)


#роут на страницу выборки квартир
@app.route('/celection')
def cele():
    return render_template('cele.html')

#запуск сервера с возможностью дебага в режиме реального времени
if __name__ == '__main__':
    app.run(debug=True)