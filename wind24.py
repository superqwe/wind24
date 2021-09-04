# https://www.wind24.it/taranto/storico
# https://pbpython.com/pandas-html-table.html
import fileinput
import glob
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize

PATH_BASE = r'D:\Studio\Python\wind24\W'

N2_KM_H = 1.852


# FIN = r'D:\Studio\Python\wind24\w\2103\210301a.htm'
#
# table_MN = pd.read_html(FIN)
# df = table_MN[0]
# df['V.Media'].replace(' nodi', '', regex=True, inplace=True)
#
# df = df[:-2]
# df = df[['Data', 'V.Media', 'Gradi']]
#
# df = df.astype({'V.Media': 'float'})
#
# df['v'] = df['V.Media'] * N2_KM_H
# df.drop(columns=['V.Media'], inplace=True)
# print(df)


def lista_dir_mesi():
    ldir = os.listdir(PATH_BASE)
    path_dir = [os.path.join(PATH_BASE, x) for x in ldir]
    return path_dir


def leggi_dati(nfile):
    print(nfile)
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
    direzioni = [
        'N',
        'NE',
        'E',
        'SE',
        'S',
        'SO',
        'O',
        'NO'
    ]
    df['dir'] = np.select(conditions, direzioni, default=None)

    # df = df[['Data', 'v', 'Gradi', 'Direzione', 'dir']]
    df = df[['Data', 'v', 'dir']]
    return (df)


def analizza_mese(df):
    pass


if __name__ == '__main__':
    lista_dir_mesi()

    df = pd.DataFrame(columns=['Data', 'v', 'dir'])

    for mese in lista_dir_mesi():
        os.chdir(mese)
        lhtml = glob.glob('*.htm')

        frames = []
        for htm in lhtml:
            frame = leggi_dati(htm)
            frames.append(frame)

        df = pd.concat(frames)

        analizza_mese(df)

        break
