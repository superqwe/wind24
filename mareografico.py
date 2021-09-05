# https://www.mareografico.it/?session=0S335644337466B66NV67Z71&syslng=ita&sysmen=-1&sysind=-1&syssub=-1&sysfnt=0&code=STAZ&idst=1C&idreq=3@4@2

import calendar
import datetime
import glob
import os
from pprint import pprint as pp

import numpy as np
import pandas as pd

ANNO = 2021
MESE = 3

PATH = r'D:\Studio\Python\wind24\mareografico'


def leggi_dati():
    lfile = os.listdir(PATH)

    ldf = []
    for nfile in lfile:
        path = os.path.join(PATH, nfile)
        df = pd.read_csv(path, sep=';', na_values='-', decimal=',')
        ldf.append(df)

    df = pd.concat(ldf)
    return df


def gradi2settore(df):
    dg = 45 / 2
    conditions = [
        (df['DIR'] > 315 + dg) | (df['DIR'] <= 45 - dg),
        (df['DIR'] > 45 - dg) & (df['DIR'] <= 45 + dg),
        (df['DIR'] > 90 - dg) & (df['DIR'] <= 90 + dg),
        (df['DIR'] > 135 - dg) & (df['DIR'] <= 135 + dg),
        (df['DIR'] > 180 - dg) & (df['DIR'] <= 180 + dg),
        (df['DIR'] > 225 - dg) & (df['DIR'] <= 225 + dg),
        (df['DIR'] > 270 - dg) & (df['DIR'] <= 270 + dg),
        (df['DIR'] > 315 - dg) & (df['DIR'] <= 315 + dg),
    ]
    direzioni = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
    df['dir'] = np.select(conditions, direzioni, default=None)

    df.rename(columns={'DATA': 'data', 'ORA': 'ora', 'DIR': 'gradi', 'VEL': 'vel'}, inplace=True)

    df.loc[df['vel'] < 5.0, 'dir'] = 'C'

    return df


if __name__ == '__main__':
    dati = leggi_dati()
    dati = gradi2settore(dati)
