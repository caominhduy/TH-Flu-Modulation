"""
This module merges temperature, humidity, and influenza data together
"""

import pandas as pd
import ast

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def merge_flu(path='data/epidemiology/processed_CDC_2008_2021.csv'):
    df = pd.read_csv(path, low_memory=False)
    df['week'] = df['week'].astype('int')
    df['year'] = df['year'].astype('int')
    cols = ['state', 'week', 'year', 'level']
    df = df.reindex(columns=cols)
    return df

def merge_weather():
    with open('data/geodata/state_abbr.txt', 'r') as f:
        contents = f.read()
        state_abbr_dict = ast.literal_eval(contents)

    states = list(state_abbr_dict.values())

    df_temp = pd.DataFrame(columns=['week', 'temp', 'state', 'year'])
    df_humid = pd.DataFrame(columns=['week', 'humid', 'state', 'year'])

    for year in list(range(2008, 2020)):
        y = str(year)
        df = pd.read_csv('data/weather/' + y + '-temp.csv')
        temps = df[states[0]]
        weeks = df['week']
        snames = pd.Series(states)
        snames = snames.repeat(len(weeks)).reset_index(drop=True)
        for s in states[1:]:
            temps = temps.append(df[s]).reset_index(drop=True)
            weeks = weeks.append(df['week']).reset_index(drop=True)
        frames = {'week': weeks, 'temp': temps, 'state': snames}
        df2 = pd.DataFrame(frames)
        df2['year'] = y
        df_temp = df_temp.append(df2)

    for year in list(range(2008, 2020)):
        y = str(year)
        df = pd.read_csv('data/weather/' + y + '-humid.csv')
        humids = df[states[0]]
        weeks = df['week']
        snames = pd.Series(states)
        snames = snames.repeat(len(weeks)).reset_index(drop=True)
        for s in states[1:]:
            humids = humids.append(df[s]).reset_index(drop=True)
            weeks = weeks.append(df['week']).reset_index(drop=True)
        frames = {'week': weeks, 'humid': humids, 'state': snames}
        df2 = pd.DataFrame(frames)
        df2['year'] = y
        df_humid = df_humid.append(df2)

    df_weather = df_temp.merge(df_humid, on=['year', 'week', 'state'])
    df_weather['week'] = df_weather['week'].astype('int')
    df_weather['year'] = df_weather['year'].astype('int')

    return df_weather

def merge():
    df_flu = merge_flu()
    df_weather = merge_weather()
    df = df_flu.merge(df_weather, on=['week', 'year', 'state'])
    df = df.sort_values(['state','week', 'year'], ignore_index=True)
    print('MERGED!')
    print(df)
    df.to_csv('data/processed.csv', index=False)
