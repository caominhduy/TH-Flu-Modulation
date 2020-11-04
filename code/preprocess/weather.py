import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import csv
import ast
import glob

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

    # Dictionary of mapping states and stations
    station_labels = {}
    with open('data/geodata/state_abbr.txt', 'r') as f:
        contents = f.read()
        state_abbr_dict = ast.literal_eval(contents)
    for id in stations['ID']:
        station_labels[id] = stations[stations['ID'] == id]['STATE'].to_list()[0]

    # # Process daily data for each station into weekly average temperature,
    # # dew point, and humidity
    # counter = 0
    # for y in list(range(2008, 2020)):
    #     input_path = 'data/weather/noaa/gsod_' + str(y)
    #     for file in os.listdir(input_path):
    #         input_full_path = input_path + '/' + file
    #         df = pd.read_csv(input_full_path,\
    #                         header=None,\
    #                         dtype={0:'str', 1:'str'},\
    #                         usecols=[0,1,2,3,4,5,6],\
    #                         names=['station', 'wban', 'date', 'temp', 'tc', 'dewp', 'dc'],\
    #                         parse_dates=['date'])
    #         df = df[df['tc']>=1]
    #         df = df[df['dc']>=1]
    #         df = df.drop(['tc', 'dc'], 1)
    #         df['id'] = df['station'] + '-' + df['wban']
    #         df = df.drop(['station', 'wban'], 1)
    #         if len(df['id'].to_list()) > 0:
    #             state = station_labels[df['id'].to_list()[0]]
    #             df['week'] = df['date'].dt.week
    #             df = df.drop(['date', 'id'], 1)
    #             df = df.groupby('week').mean()
    #             # Calculate relative humidity from temperature and dew point using
    #             # August-Roche-Magnus approximation
    #             df['c'] = (df['temp']-32)*5/9
    #             df['dewc'] = (df['dewp']-32)*5/9
    #             df['hum'] = 100*(np.exp((17.625*df['dewc'])/\
    #                             (243.04+df['dewc']))/\
    #                             np.exp((17.625*df['c'])/(243.04+df['c'])))
    #             df = df.drop(['c', 'dewc'], 1)
    #
    #             if not os.path.exists('data/weather/processed'):
    #                 os.mkdir('data/weather/processed')
    #             if not os.path.exists('data/weather/processed/'+str(y)):
    #                 os.mkdir('data/weather/processed/'+str(y))
    #
    #             output_full_path = 'data/weather/processed/' + str(y) + '/' + state +\
    #                                 '-' + file
    #             df.to_csv(output_full_path)
    #             counter += 1
    #             print(f'\rProcessed {counter} weather files', end='')
    #
    # # Merge all the processed files into annual files, labelled by year and state
    # for state in list(state_abbr_dict.values()):
    #     for year in list(range(2008, 2020)):
    #         print(f'Processing {state}, in {year}')
    #         frames = []
    #         files = glob.glob('data/weather/processed/' + str(year) + '/' + state + '*')
    #         for file in files:
    #             df = pd.read_csv(file)
    #             frames.append(df)
    #         df = pd.concat(frames).groupby('week').mean()
    #         df.to_csv('data/weather/processed/' + state + '-' + str(year) + '.csv')
    # print('\n')

    for year in list(range(2008,2020)):
        output = 'data/weather/' + str(year) + '-temp.csv'
        files = glob.glob('data/weather/processed/*-' + str(year) + '.csv')
        df = pd.read_csv(files[0])
        df = df.rename(columns={'temp': (files[0][-11] + files[0][-10])}).drop(['dewp','hum'], 1)
        for file in files[1:]:
            df_load = pd.read_csv(file)
            df_load = df_load.rename(columns={'temp': (file[-11] + file[-10])}).drop(['dewp','hum'], 1)
            df = df.merge(df_load, on='week', how='outer')
        df.to_csv(output, index=False)

    for year in list(range(2008,2020)):
        output = 'data/weather/' + str(year) + '-humid.csv'
        files = glob.glob('data/weather/processed/*-' + str(year) + '.csv')
        df = pd.read_csv(files[0])
        df = df.rename(columns={'hum': (files[0][-11] + files[0][-10])}).drop(['dewp','temp'], 1)
        for file in files[1:]:
            df_load = pd.read_csv(file)
            df_load = df_load.rename(columns={'hum': (file[-11] + file[-10])}).drop(['dewp','temp'], 1)
            df = df.merge(df_load, on='week', how='outer')
        df.to_csv(output, index=False)

    print('\nPROCESSED WEATHER DATA!')



def preprocess(option):
    if option == 'station':
        df_catalog = preprocess_station()
        return df_catalog
    if option == 'temp':
        df_catalog = preprocess_station()
        preprocess_temperature(df_catalog)
