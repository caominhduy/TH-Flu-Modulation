import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys
import imageio
import numpy as np
from operator import itemgetter
from itertools import groupby
from scipy import stats

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def get_flu_spans(df):
    df_flu = df[df['level']>=6]
    flu_weeks = df_flu.index.to_list()
    flu_week_ranges = []
    for k,g in groupby(enumerate(flu_weeks),lambda x:x[0]-x[1]):
        group = (map(itemgetter(1),g))
        group = list(map(int,group))
        if abs(group[0]-group[-1]) > 2:
            flu_week_ranges.append((group[0],group[-1]))
    for i in flu_week_ranges:
        plt.axvspan(i[0], i[1], color='red', alpha=0.2)

def regress_plot(type):
    df = pd.read_csv('data/processed.csv')

    if type == 'regplot-temp':
        slope, intercept, r_value, p_value, std_err = stats.linregress(df['temp'], df['level'])
        print(slope, intercept, r_value, p_value, std_err)
        ax = sns.regplot(x='temp', y='level', data=df, color='b', y_jitter=0.7, marker='+', line_kws={"color": "red"})
        if not os.path.exists('image/regress'):
            os.mkdir('image/regress')
        plt.savefig('image/regress/reg_temp_flu.png')
        plt.show()

    if type == 'regplot-humid':
        regress_plot = sns.regplot(x='humid', y='level', data=df)
        if not os.path.exists('image/regress'):
            os.mkdir('image/regress')
        regress_plot.figure.savefig('image/regress/reg_humid_flu.png')

    if type == 'time-series':
        state = input('Enter state name as FIPS code (e.g. "AL") ')
        df = df[df['state']==state].reset_index(drop=True)
        df['time'] = df['week'] / 52 + df['year']
        df = df.sort_values(['time'], ignore_index=True).drop(['time'], 1)
        df['time'] = df.index
        print(df)
        ax1 = plt.subplot(311)
        plt.plot('time', 'level', data=df, label='Activity Level')
        plt.setp(ax1.get_xticklabels(), visible=False)
        get_flu_spans(df)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)

        ax2 = plt.subplot(312, sharex=ax1)
        plt.plot('time', 'temp', 'r-', data=df, label='Temperature')
        plt.setp(ax2.get_xticklabels(), visible=False)
        get_flu_spans(df)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)

        ax2 = plt.subplot(313, sharex=ax1)
        plt.plot('time', 'humid', 'c-', data=df, label='RH')
        get_flu_spans(df)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
        plt.tight_layout()

        plt.savefig('image/regress/' + state + '-time-series.png')
        plt.show()

def corr_eval():
    df = pd.read_csv('data/processed.csv')
    print(df)
    print(df.corr())
