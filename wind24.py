# https://www.wind24.it/taranto/storico
# https://pbpython.com/pandas-html-table.html

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from unicodedata import normalize

N2_KM_H = 1.852

FIN = r'D:\Studio\Python\wind24\html\210301a.htm'
table_MN = pd.read_html(FIN)
df = table_MN[0]
df['V.Media'].replace(' nodi','', regex=True, inplace=True)

df = df[:-2]

df.astype({'V.Media': 'float'})

print (df.dtypes)

##df['v'] = float(df['V.Media'])
##
##print(df)
