#!/usr/bin/env python

import scipy
from scipy import stats

import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols

import wbdata
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from plotly.tools import FigureFactory as FF
#import plotly.plotly as py
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('wb_data.csv', sep='\t')
print df.head()

gdp_bins  = [-0.1, 3249,  22999.5, 140037]
gini_bins = [-0.1, 28.96, 42.97,   100]
group_names = ['Low', 'Average', 'Hight']

gdp_gini_subset = df[['iso_code','country','date','gdp', 'gini']]
#print gdp_subset.describe()
#print gini_subset.describe()
#exit (0)

gdp_gini_subset['gdp_categories'] = pd.cut(gdp_gini_subset['gdp'], gdp_bins, labels=group_names)
#print gdp_subset.head()

gdp_gini_subset['gini_categories'] = pd.cut(gdp_gini_subset['gini'], gini_bins, labels=group_names)
#print gdp_gini_subset['gini_categories'].head()
#print gdp_gini_subset['gdp_categories'].head()

'''
sns.set_context('poster')
plt.figure(figsize=(14, 7))
sns.countplot(x='gini_categories', data=gdp_gini_subset)
plt.ylabel('Count')
plt.xlabel('Economic Well-Being (GINI Index)')
plt.show()

#exit (0)

sns.set_context('poster')
plt.figure(figsize=(14, 7))
sns.countplot(x='gdp_categories', data=gdp_gini_subset)
plt.ylabel('Count')
plt.xlabel('Economic Well-Being (GDP Per Person)')
plt.show()
exit (0)
'''

#print gdp_gini_subset.head()

pisa2012_file='PISA_2012_clean.csv'
pisa12 = pd.read_csv(pisa2012_file)

pisa2015_file='PISA_2015_clean.csv'
pisa15 = pd.read_csv(pisa2015_file)

pisa2008_file='PISA_2008_clean.csv'
pisa08 = pd.read_csv(pisa2008_file)

countries = wbdata.get_country(display=False)
d = dict((x['name'].strip(), x['iso2Code']) for x in countries)

pisa12 = pisa12.assign(iso_code = pisa12.country.map(lambda x: d[x]))
pisa15 = pisa15.assign(iso_code = pisa15.country.map(lambda x: d[x]))
pisa08 = pisa08.assign(iso_code = pisa08.country.map(lambda x: d[x]))

df_pisa_all = pd.concat([pisa08, pisa12, pisa15])
df_pisa_all.sort(['country','iso_code'], inplace=True)

df4 = pd.merge(gdp_gini_subset, df_pisa_all, how='right', on=['iso_code','country','date'])
#print (df4.head())

'''
sns.set_context('poster')
plt.figure(figsize=(14, 7))
sns.countplot(x='gdp_categories', data=df4)
plt.ylabel('Count')
plt.xlabel('Economic Well-Being (GDP Per Person)')
plt.show()
exit (0)
'''

'''
H0 - hypitize that Gini index is not correlated with results in PISA test
'''
print "*******************GINI ANOVA**********************************"
pd.options.display.mpl_style = 'default'

df4.boxplot('Math', by='gini_categories', figsize=(12,8))
groups = df4.groupby("gini_categories").groups
#print groups
#exit(0)
low_gini = df4.loc[df4['gini_categories'] == 'Low'].Math
shapiro_results = scipy.stats.shapiro(low_gini)
#shapiro_results = scipy.stats.shapiro(groups["Low"])
print "*** Low GINI check normal***"
print shapiro_results

#print low_gini
av_gini =  df4.loc[df4['gini_categories'] == 'Average'].Math
shapiro_results = scipy.stats.shapiro(av_gini)
print "*** AVERAGE GINI check normal ***"
print shapiro_results


hi_gini =  df4.loc[df4['gini_categories'] == 'Hight'].Math
shapiro_results = scipy.stats.shapiro(hi_gini)
print "*** HIGHT GINI check normal ***"
print shapiro_results

#f_val, p_val = stats.f_oneway(low_gini, av_gini, hi_gini)
f_val, p_val = stats.f_oneway(groups["Low"], groups["Average"], groups["Hight"])

print "One-way ANOVA F =", f_val
print "One-way ANOVA P =", p_val

'''
Result:
    p value is much higher 
'''

print "*************************************************************"

'''
H0 - hypitize that GDP index is not correlated with results in PISA test
Can't check cause very few data with low GDP
'''
print "*******************GINI ANOVA**********************************"
'''
low_gdp = df4.loc[df4['gdp_categories'] == 'Low'].Math
shapiro_results = scipy.stats.shapiro(low_gdp)
print "*** Low GDP check normal***"
print shapiro_results

#print low_gini
av_gdp =  df4.loc[df4['gdp_categories'] == 'Average'].Math
shapiro_results = scipy.stats.shapiro(av_gdp)
print "*** AVERAGE GDP check normal ***"
print shapiro_results


hi_gdp =  df4.loc[df4['gdp_categories'] == 'Hight'].Math
shapiro_results = scipy.stats.shapiro(hi_gdp)
print "*** HIGHT GDP check normal ***"
print shapiro_results

f_val, p_val = stats.f_oneway(low_gdp, av_gdp, hi_gdp)

print "One-way ANOVA F =", f_val
print "One-way ANOVA P =", p_val 

print "*************************************************************"
'''

exit(0)

formula = 'Math ~ C(gini_categories)'
model = ols(formula, data=df4).fit()
aov_table = statsmodels.stats.anova.anova_lm(model, typ=2)
print(aov_table)
 
