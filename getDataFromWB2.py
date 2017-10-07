#!/usr/bin/env python

import requests
import pprint
import pandas as pd
import wbdata
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv

countries = [i['id'] for i in wbdata.get_country(incomelevel=['LIC','MIC','HIC'],country_id=None, display=False)]

indicators = {
            'SI.POV.GINI':'gini',
            'NY.GDP.PCAP.PP.CD':'gdp', #per capita, PPP allign
}

ind_p = {
        'LO.PISA.MAT':'Math',
        'LO.PISA.REA':'Reading',
        }

data_date = (datetime.datetime(2000, 1, 1), datetime.datetime(2017, 1, 1))

cd = wbdata.get_country(display=False)
d = dict((x['name'].strip(), x['iso2Code']) for x in cd)

df_p = wbdata.get_dataframe(
        ind_p,
        country=countries,
        data_date=data_date,
        convert_date=True,
        keep_levels=True)
df_p = df_p.reset_index()
df_p = df_p.dropna(axis=0,how='any')

df_p = df_p.assign(iso_code= df_p.country.map(lambda x: d[x]))
cols = df_p.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_p = df_p[cols]

print (df_p.tail())
df_p.to_csv('pisa_data.csv', index=False, encoding='utf-8',  sep='\t')


df = wbdata.get_dataframe(
        indicators,
        country=countries,
        data_date=data_date,
        convert_date=True,
        keep_levels=True)

dfu = df.reset_index()

dfu = dfu.assign(iso_code= dfu.country.map(lambda x: d[x]))
cols = dfu.columns.tolist()
cols = cols[-1:] + cols[:-1]
dfu = dfu[cols]

#dfu = dfu.dropna(axis=0, how='any')
dfu = dfu.fillna(method='bfill')

# CLEAN DATA

#def fx(x,y): return int(x*y/100)
#dfu5 = dfu4.assign(gdp = dfu4.gdp.map(lambda x: int(x)))

print (dfu.tail())
dfu.to_csv('wb_data2.csv', index=False, encoding='utf-8',  sep='\t')


## MERGE DATA

df_all = pd.merge(dfu, df_p, how='right', on=['iso_code', 'country', 'date'])
df_all.to_csv('data_all_clean.csv', index=False, encoding='utf-8', sep='\t')
