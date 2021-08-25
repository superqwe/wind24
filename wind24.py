# https://www.wind24.it/taranto/storico
# https://pbpython.com/pandas-html-table.html

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from unicodedata import normalize

FIN = r'D:\Studio\Python\wind24\html\210301a.htm'
table_MN = pd.read_html(FIN)
df = table_MN[0]
df['V.Media'].replace({' nodi':''}, regex=True, inplace=True)
print(df)