# http://meteotaranto.org/wxhistory.php?date=202109

import pandas as pd

# import numpy as np

ANNO = 2021
MESE = 8


def leggi_html(anno=ANNO, mese=MESE):
    path = r'D:\Studio\Python\wind24\meteotaranto\%02i%02i.htm' % (anno - 2000, mese)
    tabelle = pd.read_html(path)
    return tabelle


def analizza_dati(tabelle):
    for i, tabella in enumerate(tabelle[:-2]):
        press = tabella[1][4].split()[0]
        t_med = tabella[1][1].split('°')[0]
        t_min = tabella[1][12].split('°')[0]
        t_max = tabella[1][11].split('°')[0]
        ur = tabella[1][2][:-1]
        v_dir = tabella[1][7].split('°')[0]
        v_vel = tabella[1][6].split()[0]

        v_dir = direzione_vento(v_vel, v_dir)

        dati = i + 1, press, t_med, t_min, t_max, ur, v_dir, v_vel
        rigo = '%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s'
        print((rigo % dati).replace('.', ','))

    print('\n', tabelle[-1][0])


def direzione_vento(velocita, direzione):
    velocita = float(velocita)

    if velocita < 5.0:
        return 'Calma'

    dg = 45 / 2
    direzione = float(direzione)

    if direzione > 315 + dg or direzione <= 45 - dg:
        return 'N'
    elif 45 - dg < direzione <= 45 + dg:
        return 'NE'
    elif 90 - dg < direzione <= 90 + dg:
        return 'E'
    elif 135 - dg < direzione <= 135 + dg:
        return 'SE'
    elif 180 - dg < direzione <= 180 + dg:
        return 'S'
    elif 225 - dg < direzione <= 225 + dg:
        return 'SO'
    elif 270 - dg < direzione <= 270 + dg:
        return 'O'
    elif 315 - dg < direzione <= 315 + dg:
        return 'NO'
    else:
        return 'ERRORE'


if __name__ == '__main__':
    tabelle = leggi_html()
    analizza_dati(tabelle)
