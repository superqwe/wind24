# https://www.wind24.it/taranto/storico
# https://pbpython.com/pandas-html-table.html

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from unicodedata import normalize

N2_KM_H = 1.852

FIN = r'D:\Studio\Python\wind24\w\2103\210301a.htm'
table_MN = pd.read_html(FIN)
df = table_MN[0]
df['V.Media'].replace(' nodi', '', regex=True, inplace=True)

df = df[:-2]
df = df[['Data', 'V.Media', 'Gradi']]

df = df.astype({'V.Media': 'float'})

df['v'] = df['V.Media'] * N2_KM_H
df.drop(columns=['V.Media'], inplace=True)
print(df)
