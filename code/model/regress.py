import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys
import imageio
import numpy as np

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def regress_plot(type):
    df = pd.read_csv('data/processed.csv')
    if type == 'temp':
        regress_plot = sns.regplot(x="temp", y="level", data=df)
        if not os.path.exists('image/regress'):
            os.mkdir('image/regress')
        regress_plot.figure.savefig('image/regress/reg_temp_flu.png')
        # df_new = df.drop(['state', 'week', 'year', 'humid'], 1)
        # heatmap = sns.heatmap(df_new)
        # heatmap.figure.savefig('image/regress/heatmap.png')
        print(df.corr())
    if type == 'humid':
        regress_plot = sns.regplot(x="humid", y="level", data=df)
        if not os.path.exists('image/regress'):
            os.mkdir('image/regress')
        regress_plot.figure.savefig('image/regress/reg_humid_flu.png')
    if type == 'test':
        sns.regplot(x='temp', y='level', data=df, log_x=True)
        plt.show()
