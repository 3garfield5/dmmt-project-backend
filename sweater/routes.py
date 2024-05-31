import pandas as pd
from flask import redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import random
from catboost import CatBoostRegressor


from sweater.metro import df, metro_list
from sweater import db, app
from sweater.models import Users, BotReq, Favorites
from s3 import s3


#роут на главную страницу
@app.route('/', methods=['POST', 'GET'])
def index():
    name = request.form.get('name')
    tg = request.form.get('tg')

    if request.method == 'POST':
        bot = BotReq(name=name, tg=tg)
        db.session.add(bot)
        db.session.commit()  # добавляем данные в бд

        return render_template('go.html')

    imgs = [str(s3.generate_link(bucket='images', key=f'{i}go.svg')) for i in range(1, 6)]
    imgs2 = [str(s3.generate_link(bucket='images', key=f'go{i}.svg')) for i in range(1, 5)]
    imgs = imgs + imgs2
    imgs_out = [i for i in range(9)]
    return render_template('go.html', imgs=imgs, imgs_out=imgs_out)

#роут на страницу регистрации
@app.route('/registration', methods=['POST','GET'])
def registration():

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    # получаем данные из формы HTML

    imgs = str(s3.generate_link(bucket='images', key='Welc.svg'))

    if request.method == 'POST':
        if not (name or email or password):
            return redirect('registration')
        else:
            rep_email = db.session.query(Users.id).filter(Users.email == email)
            if db.session.query(rep_email.exists()).scalar() == False: #проверяем есть ли такая почта в БД

                hash_pwr = generate_password_hash(password) # хэшируем пароль
                new_user = Users(name=name, email=email, password=hash_pwr)
                db.session.add(new_user)
                db.session.commit() # добавляем данные в бд

                return redirect('login')

    return render_template('regist.html', imgs=imgs)

@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    rm = True if request.form.get('remainme') else False
    imgs = str(s3.generate_link(bucket='images', key='Welc.svg'))

    if email and password:
        user = Users.query.filter_by(email=email).first()

        rep_email = db.session.query(Users.id).filter(Users.email == email)
        if db.session.query(rep_email.exists()).scalar() == True: # проверяем повтор почты в БД, если есть, то выполняется условие

            if user and check_password_hash(user.password, password): # проверяем правильность пароля
                login_user(user, remember=rm) # выполняем вход в аккаунт

                return redirect('per_acc')

    return render_template('login.html', imgs=imgs)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user() # функция выхода человека из аккаунта
    return redirect(url_for('index'))

#роут на страницу личного кабинета
@app.route('/per_acc', methods=['GET'])
@login_required
def acc():
    return render_template('lk.html')

@app.route('/collection', methods=['POST', 'GET'])
def collection():
    price_bot = request.form.get('price_bot')
    price_top = request.form.get('price_top')
    region = request.form.get('region')
    ap_type = request.form.get('ap_type')
    area_bot = request.form.get('area_bot')
    area_top = request.form.get('area_top')
    renovation = request.form.get('renovation')
    metro_station = request.form.get('metro_station')
    imgs = [str(s3.generate_link(bucket='images', key=f'{i}.svg')) for i in range(1, 37)]
    imgs_out = []


    # заполнение значений, если их не заполнил пользователь
    if not price_bot:
        price_bot = min(df['Price'])
    if not price_top:
        price_top = max(df['Price'])
    if not area_bot:
        area_bot = min(df['Area'])
    if not area_top:
        area_top = max(df['Area'])

    if request.method == 'POST':
        one = request.form.get("1")
        two = request.form.get("2")

        if metro_station:
            df_filter = df.loc[(df['Price'] > abs(float(price_bot))) & (df['Price'] < abs(float(price_top))) &
            (df['Region'] == region) & (df['Apartment type'] == ap_type) & (df['Area'] > abs(float(area_bot))) &
            (df['Area'] < abs(float(area_top))) & (df['Renovation'] == renovation) & (df['Metro station'] == metro_station.lower())]
            df_filter_len = len(df_filter)
            imgs_out = df_filter.index.tolist()
            imgs_out = [(i % 37) for i in imgs_out]



        else:
            df_filter = df.loc[(df['Price'] > abs(float(price_bot))) & (df['Price'] < abs(float(price_top))) &
            (df['Region'] == region) & (df['Apartment type'] == ap_type) & (df['Area'] > abs(float(area_bot))) &
            (df['Area'] < abs(float(area_top))) & (df['Renovation'] == renovation)]
            df_filter_len = len(df_filter)
            imgs_out = df_filter.index.tolist()
            imgs_out = [i % 37 for i in imgs_out]

        if one is None and two is not None:
            if current_user.is_authenticated:
                if current_user.is_active:
                    user_id = int(current_user.get_id())
                    product_id = two
                    rep_app = db.session.query(Favorites.id).filter(Favorites.product_id == product_id)
                    if db.session.query(rep_app.exists()).scalar() == False:
                        fav = Favorites(user_id=user_id, product_id=product_id)
                        db.session.add(fav)
                        db.session.commit()




        return render_template('coll.html', df_filter=df_filter, df_filter_len=df_filter_len, imgs_out=imgs_out, imgs=imgs)
    return render_template('coll.html')

@app.route('/cost_calculation', methods=['POST', 'GET'])
def calculate():
    ap_type = request.form.get('ap_type')
    region = request.form.get('region')
    metro_station = request.form.get('metro station')
    minutes_to_metro = request.form.get('minutes to metro')
    number_of_rooms = request.form.get('number of rooms')
    area = request.form.get('area')
    liv_area = request.form.get('living area')
    kit_area = request.form.get('kitchen area')
    floor = request.form.get('floor')
    number_of_floors = request.form.get('number of floors')
    renovation = request.form.get('renovation')
    imgs = str(s3.generate_link(bucket='images', key='10.svg'))

    max_val_df_minutes_to_metro = df['Minutes to metro'].max()
    max_val_df_number_of_rooms = df['Number of rooms'].max()
    max_val_df_area = df['Area'].max()
    max_val_df_liv_area = df['Living area'].max()
    max_val_df_kit_area = df['Kitchen area'].max()
    max_val_df_floor = df['Floor'].max()
    max_val_df_number_of_floors = df['Number of floors'].max()

    min_val_df_minutes_to_metro = df['Minutes to metro'].min()
    min_val_df_number_of_rooms = df['Number of rooms'].min()
    min_val_df_area = df['Area'].min()
    min_val_df_liv_area = df['Living area'].min()
    min_val_df_kit_area = df['Kitchen area'].min()
    min_val_df_floor = df['Floor'].min()
    min_val_df_number_of_floors = df['Number of floors'].min()


    if request.method == 'POST':
        print(ap_type, region, metro_station, minutes_to_metro, number_of_rooms, number_of_floors, area, liv_area, kit_area, floor, renovation)
        if ap_type and region and metro_station and minutes_to_metro and number_of_rooms and area and liv_area and kit_area and floor and number_of_floors and renovation:

            if ((float(liv_area) + float(kit_area)) <= float(area)) and (int(floor) <= int(number_of_floors)) and (metro_station.strip().lower() in metro_list):

                if (int(number_of_rooms) < max_val_df_number_of_rooms) and (int(number_of_rooms) > min_val_df_number_of_rooms) and \
                    (float(area) < max_val_df_area) and (float(area) > min_val_df_area) and \
                    (float(liv_area) < max_val_df_liv_area) and (float(liv_area) > min_val_df_liv_area) and \
                    (float(kit_area) < max_val_df_kit_area) and (float(kit_area) > min_val_df_kit_area) and \
                    (int(floor) < max_val_df_floor) and (int(floor) > min_val_df_floor) and \
                    (int(number_of_floors) < max_val_df_number_of_floors) and (int(number_of_floors) > min_val_df_number_of_floors) and \
                    (int(minutes_to_metro) < max_val_df_minutes_to_metro ) and (int(minutes_to_metro) > min_val_df_minutes_to_metro):

                    x_calc = pd.Series({'Apartment type': ap_type, 'Metro station': metro_station,
                                        'Minutes to metro': minutes_to_metro, 'Region': region,
                                        'Number of rooms': number_of_rooms, 'Area': area,
                                        'Living area': liv_area, 'Kitchen area': kit_area,
                                        'Floor': floor, 'Number of floors': number_of_floors,
                                        'Renovation': renovation})
                    flag = True
                    model = CatBoostRegressor()
                    model.load_model('sweater/house_model',
                                     format='cbm')
                    prediction = round(model.predict(x_calc))
                    return render_template('calk.html', prediction=prediction, flag=flag, area=area, imgs=imgs)

                else:
                    flash('Были введены долвольно большие (или наборот маленькие) значения, из-за чего цена может не соостветсвовать действительности!')
            else:
                flash('Вы ввели неккоректные данные! К примеру: ')
                flash('1) сумма кухонной площади и жилой больше, чем общая площадь')
                flash('2) вы выбрали этаж, который превышает количество этажей в доме')
                flash('3) была неправильно указана станция метро')
        else:
            flash('Вы ввели не все значения!')


    return render_template('calk.html')

@app.route('/fav', methods=['POST', 'GET'])
@login_required
def favourites():
    user_id = int(current_user.get_id())
    db_fav_app = db.session.query(Favorites).filter(user_id == Favorites.user_id)
    fav_app = list(map(lambda x: x.product_id, db_fav_app))
    len_fav_app = len(fav_app)
    imgs = [str(s3.generate_link(bucket='images', key=f'{i}.svg')) for i in range(1, 37)]
    imgs_out = [i % 37 for i in fav_app]

    one = request.form.get('1')
    if request.method == 'POST':

        del_app = db.session.query(Favorites).filter(Favorites.product_id == one and Favorites.user_id == user_id).first()
        db.session.delete(del_app)
        db.session.commit()

        db_fav_app = db.session.query(Favorites).filter(user_id == Favorites.user_id)
        fav_app = list(map(lambda x: x.product_id, db_fav_app))
        fav_app = set(fav_app)
        fav_app = list(fav_app)
        len_fav_app = len(fav_app)

        return render_template('izb.html', fav_app=fav_app, len_fav_app=len_fav_app, df=df, imgs=imgs, imgs_out=imgs_out)
    return render_template('izb.html', fav_app=fav_app, len_fav_app=len_fav_app, df=df, imgs=imgs, imgs_out=imgs_out)

@app.route('/about')
def about():
    imgs = [str(s3.generate_link(bucket='images', key='down.svg')),
            str(s3.generate_link(bucket='images', key='l_d.svg')),
            str(s3.generate_link(bucket='images', key='left.svg')),
            str(s3.generate_link(bucket='images', key='r_d.svg')),
            str(s3.generate_link(bucket='images', key='right.svg'))]
    return render_template('about.html', imgs=imgs)

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
