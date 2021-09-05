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
    pass


if __name__ == '__main__':
    dati = leggi_dati()
    gradi2settore(dati)
