from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('admin.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS per_acc (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, password TEXT NOT NULL)')
    conn.close()

def close_db_connection(conn):
    conn.close()

def delete():
    conn = get_db_connection()
    conn.execute('DELETE from per_acc')
    conn.commit()
    conn.close()

@app.before_request
def before_first_request():
    init_db()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect('/admin')
    return render_template('index.html')

@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO per_acc (login, password) VALUES (?, ?)', (login, password))
            conn.commit()
            conn.close()
            return redirect('/per_acc')
        except:
            return 'Ошибка'

    return render_template('admin.html')

@app.route('/boute')
def aboute():
    return render_template('boute.html')

@app.route('/per_acc')
def acc():
    return render_template('per_acc.html')

@app.route('/celection')
def cele():
    return render_template('cele.html')

if __name__ == '__main__':
    app.run(debug=True)