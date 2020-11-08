import plotly.express as px
import plotly.io as pio
import chart_studio.tools as tls
import plotly.graph_objects as go
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import json
import imageio
import glob

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def epi_graph(df, ss, wk):
    df = df[df['year'] == ss]
    df = df[df['week'] == wk]
    fig = px.choropleth(df, \
                        locations='state',\
                        locationmode = 'USA-states',\
                        color='level',\
                        color_continuous_scale="Spectral_r",\
                        range_color=(0, 13),\
                        hover_name='state',\
                        hover_data={'state':False},\
                        scope="usa",\
                        labels={'level':'Level'},\
                        width=1100,\
                        height=600)
    fig.update_layout(
        title=ss+' - Week '+str(wk),
        title_x=0.5,
        title_font_size=25)

    if not os.path.exists('image/epidemiology/' + ss):
        os.mkdir('image/epidemiology/' + ss)

    pio.write_image(fig, file='image/epidemiology/'+ ss + '/' + \
                    ss + 'W' + str(wk) + '.png')

# Take processed epidemiological data as input and output:
#   - Choropleth maps for each year and week as
#   - Combine separate maps of each year into GIFs
def epi_render(df):
    # Handle exceptions
    if not os.path.exists('image'):
        os.mkdir('image')
    if not os.path.exists('image/epidemiology'):
        os.mkdir('image/epidemiology')

    # Make static images (may take a while for >600 maps)
    counter = 0
    for year in df['year'].unique():
        df_filtered = df[df['year']==year]
        for week in df_filtered['week'].unique():
            epi_graph(df, year, week)
            counter += 1
            if counter == 1:
                print(f'\r Generated {counter} map', end='')
            else:
                print(f'\r Generated {counter} maps', end='')

    print('\n')

    # Make GIF images for each year
    counter = 0

    for year in df['year'].unique():
        prefix = 'image/epidemiology/' + year + '/' + year + 'W'
        filenames = []
        for i in range(53):
            p = prefix + str(i) + '.png'
            if os.path.exists(p):
                filenames.append(p)
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('image/epidemiology/' + year + '/' + year + '.gif', images)
        counter += 1
        if counter == 1:
            print(f'\r Generated {counter} GIF', end='')
        else:
            print(f'\r Generated {counter} GIFs', end='')

# Graph the weather station locations
def station_render(df, name):
    fig = go.Figure(data=go.Scattergeo(lon = df['LON'],\
                                        lat = df['LAT'],\
                                        text = df['STATION NAME'],\
                                        mode = 'markers',\
                                        marker_color = 'dodgerblue'
                                        ))

    fig.update_layout(
            title = 'US Weather Stations (filtered)',\
            title_x=0.5,\
            title_font_size=16,\
            geo_scope='usa',
            width=1100,
            height=600)

    if not os.path.exists('image/'):
        os.mkdir('image')
    if not os.path.exists('image/weather/'):
        os.mkdir('image/weather')
    pio.write_image(fig, file='image/weather/'+ name + '.png')

def temp_render():
    counter = 0
    for year in list(range(2008, 2020)):
        df = pd.read_csv('data/weather/' + str(year)+'-temp.csv')
        weeks = df['week'].to_list()
        for week in weeks:
            df_new = df[df['week'] == week]
            df_new = df_new.drop(['week'], 1).reset_index(drop=True).T
            df_new['state'] = df_new.index
            df_new = df_new.rename(columns={0:'temp'})

            fig = px.choropleth(df_new, \
                                locations='state',\
                                locationmode = 'USA-states',\
                                color='temp',\
                                color_continuous_scale="Spectral_r",\
                                range_color=(0, 100),\
                                hover_name='state',\
                                hover_data={'state':False},\
                                scope="usa",\
                                labels={'temp':'Temp (oF)'},\
                                width=1100,\
                                height=600)
            fig.update_layout(
                title=str(year) + ' - Week ' + str(week),
                title_x=0.5,
                title_font_size=25)

            if not os.path.exists('image/weather/' + str(year)):
                os.mkdir('image/weather/' + str(year))
            if not os.path.exists('image/weather/' + str(year) + '/temp'):
                os.mkdir('image/weather/' + str(year) + '/temp')

            pio.write_image(fig, file='image/weather/'+ str(year) + '/temp/' + \
                            str(year) + 'W' + str(week) + '.png')
            counter += 1
            if counter == 1:
                print(f'\r Generated {counter} map', end='')
            else:
                print(f'\r Generated {counter} maps', end='')

        prefix = 'image/weather/' + str(year) + '/temp/' + str(year) + 'W'
        filenames = []
        for i in range(53):
            p = prefix + str(i) + '.png'
            if os.path.exists(p):
                filenames.append(p)
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('image/weather/' + str(year) + '/temp/' + str(year) + '.gif', images)
    print('\n Finished rendering temperature graphs')

def humid_render():
    counter = 0
    for year in list(range(2008, 2020)):
        df = pd.read_csv('data/weather/' + str(year)+'-humid.csv')
        weeks = df['week'].to_list()
        for week in weeks:
            df_new = df[df['week'] == week]
            df_new = df_new.drop(['week'], 1).reset_index(drop=True).T
            df_new['state'] = df_new.index
            df_new = df_new.rename(columns={0:'humid'})

            fig = px.choropleth(df_new, \
                                locations='state',\
                                locationmode = 'USA-states',\
                                color='humid',\
                                color_continuous_scale="Spectral_r",\
                                range_color=(0, 100),\
                                hover_name='state',\
                                hover_data={'state':False},\
                                scope="usa",\
                                labels={'humid':'Humidity'},\
                                width=1100,\
                                height=600)
            fig.update_layout(
                title=str(year) + ' - Week ' + str(week),
                title_x=0.5,
                title_font_size=25)

            if not os.path.exists('image/weather/' + str(year)):
                os.mkdir('image/weather/' + str(year))
            if not os.path.exists('image/weather/' + str(year) + '/humid'):
                os.mkdir('image/weather/' + str(year) + '/humid')

            pio.write_image(fig, file='image/weather/'+ str(year) + '/humid/' + \
                            str(year) + 'W' + str(week) + '.png')
            counter += 1
            if counter == 1:
                print(f'\r Generated {counter} map', end='')
            else:
                print(f'\r Generated {counter} maps', end='')

        prefix = 'image/weather/' + str(year) + '/humid/' + str(year) + 'W'
        filenames = []
        for i in range(53):
            p = prefix + str(i) + '.png'
            if os.path.exists(p):
                filenames.append(p)
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('image/weather/' + str(year) + '/humid/' + str(year) + '.gif', images)
    print('\n Finished rendering humidity graphs')

def weather_render():
    temp_render()
    humid_render()
