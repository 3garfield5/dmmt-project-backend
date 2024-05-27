import pandas as pd

df = pd.read_csv('sweater/static/data.csv')

"""Исправление ошибки с количеством станций метро"""

df['Metro station'].nunique() # станций метро в Москве точно меньше

len(set(map(lambda x: x.strip().lower(), df['Metro station'])))

df['Metro station'] = list(map(lambda x: x.strip().lower(), df['Metro station']))

metro = df['Metro station'].drop_duplicates()

metro_list = []

for i in metro:
    metro_list.append(i)

metro_list_1 = metro_list[:103]
metro_list_2 = metro_list[103:206]
metro_list_3 = metro_list[206:310]


