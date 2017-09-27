#!/usr/bin/env python


import requests
import pprint
import pandas as pd
import wbdata
import matplotlib.pyplot as plt
import numpy as np
import wbdata
import datetime

pisa2012_file='PISA_2012_clean.csv'
df2 = pd.read_csv(pisa2012_file)

pisa2015_file='PISA_2015_clean.csv'
df2015 = pd.read_csv(pisa2015_file)

pisa2008_file='PISA_2008_clean.csv'
df2008 = pd.read_csv(pisa2008_file)

countries = wbdata.get_country(display=False)
d = dict((x['name'].strip(), x['iso2Code']) for x in countries)

df3 = df2.assign(iso_code = df2.country.map(lambda x: d[x]))
df2015_1 = df2015.assign(iso_code = df2015.country.map(lambda x:d[x]))
df2008_1 = df2008.assign(iso_code = df2008.country.map(lambda x:d[x]))

df1 = pd.read_csv('wb_data.csv', sep='\t')

df_pisa_all = pd.concat([df2008_1, df3, df2015_1])
df_pisa_all.sort(['country','iso_code'], inplace=True)
#print(df_pisa_all)
#exit(0)

df4 = pd.merge(df1, df_pisa_all, how='right', on=['iso_code','country','date'])

print (df4.head())

df4.to_csv('data.csv', index=False, encoding='utf-8',  sep='\t')
