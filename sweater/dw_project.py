import pandas as pd
import random

df = pd.read_csv('sweater/static/data.csv')

"""Исправление ошибки с количеством станций метро"""

df['Metro station'].nunique() # станций метро в Москве точно меньше

len(set(map(lambda x: x.strip().lower(), df['Metro station'])))

df['Metro station'] = list(map(lambda x: x.strip().lower(), df['Metro station']))

df['Metro station'].nunique()

metro = df['Metro station'].drop_duplicates()

metro_list = []

for i in metro:
    metro_list.append(i)


