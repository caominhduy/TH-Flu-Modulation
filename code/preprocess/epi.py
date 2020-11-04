import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import csv
import ast
import json

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def preprocess(path='data/epidemiology/CDC_2008_2021.csv'):
    df = pd.read_csv(path,\
                    header=0,\
                    low_memory=False,\
                    usecols=['STATENAME', 'ACTIVITY LEVEL', 'WEEK', 'WEEKEND'],
                    parse_dates=['WEEKEND'])

    df['YEAR'] = df['WEEKEND'].dt.year
    df = df.drop(['WEEKEND'], 1)

    with open('data/geodata/state_abbr.txt', 'r') as f:
        contents = f.read()
        state_abbr_dict = ast.literal_eval(contents)

    # Filter state records only
    df = df[df['STATENAME'].isin(state_abbr_dict)]

    # Check if there has been enough data for every year
    year_hashmap = {}
    for year in df['YEAR'].unique():
        df_filtered = df[df['YEAR'] == year]
        number_of_states = len(df_filtered['STATENAME'].unique())
        year_hashmap[year] = number_of_states
        print(f'For year {year}: {number_of_states} states are on records')

    # Simplify the headers and names for convenience
    df = df.rename(columns={'STATENAME':'state',\
                            'ACTIVITY LEVEL': 'level',\
                            'WEEK': 'week',\
                            'YEAR': 'year'})

    df['level'] = df['level'].str.replace('Level ', '')
    df['level'] = df['level'].astype('int32')
    df['year'] = df['year'].astype('str')
    df['state'] = df['state'].replace(state_abbr_dict)

    df.to_csv('data/epidemiology/processed_CDC_2008_2021.csv', index=False)
    print('\n', '[SUCCESS] Preprocessed')
    print(df)
    return df
