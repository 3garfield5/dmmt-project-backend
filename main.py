from sweater import app, db

# with app.app_context():
#     db.create_all()

#запуск сервера с возможностью дебага в режиме реального времени
if __name__ == '__main__':
    app.run(debug=True)