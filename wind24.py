# https://www.wind24.it/taranto/storico
# https://pbpython.com/pandas-html-table.html
import calendar
import datetime
import glob
import os
from pprint import pprint as pp

import numpy as np
import pandas as pd

ANNO = 2021
MESE = 3

PATH_BASE = r'D:\Studio\Python\wind24\W'
N2_KM_H = 1.852


def lista_dir_mesi():
    ldir = os.listdir(PATH_BASE)
    path_dir = [os.path.join(PATH_BASE, x) for x in ldir if os.path.isdir(os.path.join(PATH_BASE, x))]
    return path_dir


def leggi_dati(nfile):
    # print(nfile)
    table_MN = pd.read_html(nfile)
    df = table_MN[0]
    df['V.Media'].replace(' nodi', '', regex=True, inplace=True)

    df = df[:-2]

    df = df.astype({'V.Media': 'float'})

    # velocità in km/h
    df['v'] = df['V.Media'] * N2_KM_H

    # direzione in quadranti
    dg = 45 / 2
    conditions = [
        (df['Gradi'] > 315 + dg) | (df['Gradi'] <= 45 - dg),
        (df['Gradi'] > 45 - dg) & (df['Gradi'] <= 45 + dg),
        (df['Gradi'] > 90 - dg) & (df['Gradi'] <= 90 + dg),
        (df['Gradi'] > 135 - dg) & (df['Gradi'] <= 135 + dg),
        (df['Gradi'] > 180 - dg) & (df['Gradi'] <= 180 + dg),
        (df['Gradi'] > 225 - dg) & (df['Gradi'] <= 225 + dg),
        (df['Gradi'] > 270 - dg) & (df['Gradi'] <= 270 + dg),
        (df['Gradi'] > 315 - dg) & (df['Gradi'] <= 315 + dg),
    ]
    direzioni = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
    df['dir'] = np.select(conditions, direzioni, default=None)

    df.loc[df['v'] < 5.0, 'dir'] = 'C'

    # df = df[['Data', 'v', 'Gradi', 'Direzione', 'dir']]
    df = df[['Data', 'v', 'dir']]
    # print(df)
    return (df)


def analizza_mese(df, anno, mese):
    data_inizio = datetime.date(anno, mese, 1)
    data_fine = datetime.date(anno, mese, calendar.monthrange(anno, mese)[1])
    date_range = pd.date_range(data_inizio, data_fine)

    dati = []
    for giorno in date_range:
        data = giorno.strftime('%d/%m/%Y')
        df1 = df[df['Data'] == data]

        # velocità media
        v = df1['v'].mean()

        if np.isnan(v) or v < 5.0:
            direzione = 'V'
        else:
            # direzione dominante
            print(df1.groupby('dir').count())
            df2 = df1.drop(df1[df1['dir'] == 'C'].index)
            direzione = df2.dir.mode().values[0]
            print(data, '---', direzione, '\n' * 3)

        #
        dati.append([data, v, direzione])

    pp(dati)

    return


if __name__ == '__main__':
    df = pd.DataFrame(columns=['Data', 'v', 'dir'])

    for mese in lista_dir_mesi():
        print('\n---' * 3, mese)
        os.chdir(mese)
        lhtml = glob.glob('*.htm')

        frames = []
        for htm in lhtml:
            frame = leggi_dati(htm)
            frames.append(frame)

        df = pd.concat(frames)

        analizza_mese(df, ANNO, MESE)
        break
