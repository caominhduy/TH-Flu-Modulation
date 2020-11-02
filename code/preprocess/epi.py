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
                    usecols=['STATENAME', 'ACTIVITY LEVEL', 'WEEK', 'SEASON'])

    with open('data/geodata/state_abbr.txt', 'r') as f:
        contents = f.read()
        state_abbr_dict = ast.literal_eval(contents)

    # Filter state records only
    df = df[df['STATENAME'].isin(state_abbr_dict)]

    # Check if there has been enough data for every season
    season_hashmap = {}
    for season in df['SEASON'].unique():
        df_filtered = df[df['SEASON'] == season]
        number_of_states = len(df_filtered['STATENAME'].unique())
        season_hashmap[season] = number_of_states
        print(f'For season {season}: {number_of_states} states are on records')

    # Simplify the headers and names for convenience
    df = df.rename(columns={'STATENAME':'state',\
                            'ACTIVITY LEVEL': 'level',\
                            'WEEK': 'week',\
                            'SEASON': 'season'})
    df['level'] = df['level'].str.replace('Level ', '')
    df['level'] = df['level'].astype('int32')
    df['state'] = df['state'].replace(state_abbr_dict)

    print('\n', '[SUCCESS] Preprocessed')
    print(df)
    return df
