# https://www.mareografico.it/?session=0S335644337466B66NV67Z71&syslng=ita&sysmen=-1&sysind=-1&syssub=-1&sysfnt=0&code=STAZ&idst=1C&idreq=3@4@2

import calendar
import datetime
import glob
import os
from pprint import pprint as pp

import numpy as np
import pandas as pd
import sqlite3 as db

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


def salva_sqlite(df):
    con = db.connect('ispra.sqlite')
    df.to_sql('ISPRA', con, if_exists='replace')


def analizza_mese(df, anno=ANNO, mese=MESE):
    data_inizio = datetime.date(anno, mese, 1)
    data_fine = datetime.date(anno, mese, calendar.monthrange(anno, mese)[1])
    date_range = pd.date_range(data_inizio, data_fine)

    dati = []
    for giorno in date_range:
        data = int(giorno.strftime('%Y%m%d'))
        df1 = df[df['data'] == data]

        # velocità media
        v = df1['vel'].mean()

        if False:
            pass
        # if np.isnan(v) or v < 5.0:
        #     direzione = 'V'
        else:
            # direzione dominante
            print(df1.groupby('dir').count())
            df2 = df1.drop(df1[df1['dir'] == 'C'].index)

            try:
                direzione = df2.dir.mode().values[0]
            except IndexError:
                print('***', 'tutto il giorno calma di vento')
                direzione = 'Variabile'

            print(data, '---', direzione, '\n' * 3)

        #
        dati.append([giorno.strftime('%d/%m/%Y'), v, direzione])

    # pp(dati)
    return dati


def scrivi_dati(dati):
    righi = ['%s\t%.1f\t%s' % (data, vel, settore) for data, vel, settore in dati]
    tabella = '\n'.join(righi)
    print(tabella)


if __name__ == '__main__':
    dati = leggi_dati()
    dati = gradi2settore(dati)
    salva_sqlite(dati)
    dati = analizza_mese(dati)
    scrivi_dati(dati)
