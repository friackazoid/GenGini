#!/usr/bin/env python

import requests
import pprint
import pandas as pd
import wbdata
import matplotlib.pyplot as plt
import numpy as np
import datetime

countries = ["AR","BR","CO","CL","MX","PE"]

indicators = {
            'SI.POV.GINI':'gini',
            'NY.GDP.PCAP.PP.CD':'gdp', #per capita, PPP allign
}

data_date = (datetime.datetime(2000, 1, 1), datetime.datetime(2017, 1, 1))

df = wbdata.get_dataframe(
        indicators,
        country="all",
        data_date=data_date,
        convert_date=True,
        keep_levels=True)

dfu = df.reset_index()
#print(dfu.tail())

countries = wbdata.get_country(display=False)
d = dict((x['name'].strip(), x['iso2Code']) for x in countries)

dfu2 = dfu.assign(iso_code= dfu.country.map(lambda x: d[x]))
cols = dfu2.columns.tolist()
cols = cols[-1:] + cols[:-1]
dfu3 = dfu2[cols]
#print (dfu3.tail())

dfu4 = dfu3.fillna(method='bfill')
print (dfu4.tail())

#dfu4.to_csv('wb_data.csv', index=False, encoding='utf-8',  sep='\t')

# CLEAN DATA

def fx(x,y): return int(x*y/100)
dfu5 = dfu4.assign(gdp = dfu4.gdp.map(lambda x: int(x)))

print (dfu5.tail())
dfu5.to_csv('wb_data.csv', index=False, encoding='utf-8',  sep='\t')

