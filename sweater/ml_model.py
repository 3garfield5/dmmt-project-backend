from dw_project import df
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor, Pool

X = df.drop(['Price'], axis=1)
y = df['Price']

X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.7, shuffle=True)

# выделим категориальные признаки
cat_features = ['Apartment type', 'Metro station', 'Region', 'Renovation']

train_data = Pool(data=X_train, label=y_train, cat_features=cat_features)
val_data = Pool(data=X_val, label=y_val, cat_features=cat_features)
full_data = Pool(data=X, label=y, cat_features=cat_features)

model = CatBoostRegressor(loss_function = 'MAPE')

model.fit(train_data,
          eval_set=val_data,
          verbose=False,
          plot=True)