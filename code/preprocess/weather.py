import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import csv
import ast
import json
import gzip

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def preprocess_station():
    """
    Header Description by NOAA:
    USAF = Air Force station ID. May contain a letter in the first position.
    WBAN = NCDC WBAN number
    CTRY = FIPS country ID
    ST = State for US stations
    ICAO = ICAO ID
    LAT = Latitude in thousandths of decimal degrees
    LON = Longitude in thousandths of decimal degrees
    ELEV = Elevation in meters
    BEGIN = Beginning Period Of Record (YYYYMMDD). There may be reporting gaps within the P.O.R.
    END = Ending Period Of Record (YYYYMMDD). There may be reporting gaps within the P.O.R.
    """
    df_catalog = pd.read_csv('data/weather/noaa/isd-history.csv',\
                            header=0,\
                            low_memory=False,\
                            usecols=['USAF', 'WBAN', 'STATION NAME', 'CTRY', 'STATE',\
                                    'LAT', 'LON', 'BEGIN', 'END'])

    with open('data/geodata/state_abbr.txt', 'r') as f:
        contents = f.read()
        state_abbr_dict = ast.literal_eval(contents)

    # Filter valid US stations
    df_catalog = df_catalog[df_catalog['CTRY'] == 'US']
    df_catalog = df_catalog.drop(['CTRY'], 1)
    df_catalog = df_catalog[df_catalog['STATE'].isin(state_abbr_dict.values())]
    df_catalog = df_catalog[df_catalog['USAF'].isin(map(str,list(range(0,999999+1))))]

    # Filter stations that cover the research range
    df_catalog = df_catalog[df_catalog['END']>=20190416]
    df_catalog = df_catalog[df_catalog['BEGIN']<20080928].reset_index(drop=True)

    # Clean up repository by removal of unnecessary weather data
    df_catalog['WBAN'] = df_catalog['WBAN'].astype('str')
    df_catalog['ID'] = df_catalog['USAF'] + '-' + df_catalog['WBAN']
    stations = df_catalog['ID'].to_list()
    pre_path = 'data/weather/noaa/gsod_'
    counter = 0
    for year in map(str,list(range(2008, 2020))):
        path = pre_path + year + '/'
        for file in os.listdir(path):
            f = file.split('-')[0] + '-' + file.split('-')[1]
            if f not in stations:
                p = path + f + '-' + year + '.op.gz'
                os.remove(p)
                counter += 1
    print(f'{counter} unnecessary files are found and removed')

    return df_catalog

def op_to_csv(path):
    new_path = path.replace('.op', '.csv')
    with open(path, 'r') as op, open(new_path, 'w') as o:
        lines = []
        for line in op:
            line = line.replace(' ',',')
            new_line = line[0]
            for i in range(1, len(line)):
                if line[i-1] != ',' or line[i] != ',':
                    new_line = new_line + line[i]
            lines.append(new_line)
        o.writelines(lines[1:])

def preprocess_temperature(stations):
    # Convert all the OP files into readable CSV files
    pre_path = 'data/weather/noaa/gsod_'
    counter = 0
    for year in map(str,list(range(2008, 2020))):
        path = pre_path + year + '/'
        for file in os.listdir(path):
            if file.split('.')[-1] == 'op':
                op_to_csv(path + file)
                os.remove(path + file)
                counter += 1
    print(f'{counter} OP files have been converted into CSV files')



def preprocess(option):
    if option == 'station':
        df_catalog = preprocess_station()
        return df_catalog
    if option == 'temp':
        df_catalog = preprocess_station()
        preprocess_temperature(df_catalog)
