import plotly.express as px
import plotly.io as pio
import chart_studio.tools as tls
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
    df = df[df['season'] == ss]
    df = df[df['week'] == wk]
    fig = px.choropleth(df, \
                        locations='state',\
                        locationmode = 'USA-states',\
                        color='level',\
                        color_continuous_scale="Spectral_r",\
                        range_color=(0, 10),\
                        hover_name='state',\
                        hover_data={'state':False},\
                        scope="usa",\
                        labels={'level':'Level'},\
                        width=1100,\
                        height=600)
    fig.update_layout(
        title='Season '+ss+' - Week '+str(wk),
        title_x=0.5,
        title_font_size=25)

    if not os.path.exists('image/epidemiology/' + ss):
        os.mkdir('image/epidemiology/' + ss)

    pio.write_image(fig, file='image/epidemiology/'+ ss + '/' + \
                    ss + 'W' + str(wk) + '.png')

def epi_render(df):
    # Handle exceptions
    if not os.path.exists('image'):
        os.mkdir('image')
    if not os.path.exists('image/epidemiology'):
        os.mkdir('image/epidemiology')

    # Make static images (may take a while for >600 maps)
    counter = 0
    for season in df['season'].unique():
        df_filtered = df[df['season']==season]
        for week in df_filtered['week'].unique():
            epi_graph(df, season, week)
            counter += 1
            if counter == 1:
                print(f'\r Generated {counter} map', end='')
            else:
                print(f'\r Generated {counter} maps', end='')

    print('\n')

    # Make GIF images for each season
    counter = 0

    for season in df['season'].unique():
        prefix = 'image/epidemiology/' + season + '/' + season + 'W'
        filenames = []
        for i in range(53):
            p = prefix + str(i) + '.png'
            if os.path.exists(p):
                filenames.append(p)
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('image/epidemiology/' + season + '/' + season + '.gif', images)
        counter += 1
        if counter == 1:
            print(f'\r Generated {counter} GIF', end='')
        else:
            print(f'\r Generated {counter} GIFs', end='')
