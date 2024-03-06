#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\NSFG') 

#%%Imports
import pandas as pd
import numpy as np
import scipy.stats as stats 
import matplotlib.pyplot as plt

#%%read in variables of interest
selectvars = pd.read_excel(f'number_of_partners - variables of interest.xlsx')

#%%read in datasets
startyears = [2006,2011,2013,2015,2017]
endyears = [2010,2013,2015,2017,2019]

df_male = {}
df_male_full = pd.DataFrame(columns=selectvars['Variable name'])
df_female = {}
df_female_full = pd.DataFrame(columns=selectvars['Variable name'])
for start, end in zip(startyears,endyears):
    df_male[f'data_{start}_{end}'] = pd.read_csv(f'data downloads/male data/{start}_{end}_MaleData.csv', na_values = [' ','NA','inf'], index_col=0)[selectvars['Variable name']]
    df_male_full = pd.concat([df_male_full,df_male[f'data_{start}_{end}']])
    
    df_female[f'data_{start}_{end}'] = pd.read_csv(f'data downloads/female data/{start}_{end}_FemaleData.csv', na_values = [' ','NA','inf'], index_col=0)[selectvars['Variable name']]
    df_female_full = pd.concat([df_female_full,df_female[f'data_{start}_{end}']])

#%%make cols numeric

df_male_full['AGE_R'] = df_male_full['AGE_R'].astype('int64')
df_male_full['LIFPRTNR'] = df_male_full['LIFPRTNR'].astype('int64')
df_male_full_virgins = df_male_full[df_male_full['LIFPRTNR']==0]
df_male_full.loc[df_male_full_virgins.index,'PARTS1YR'] = 0
df_male_full['PARTS1YR'] = df_male_full['PARTS1YR'].astype('int64')
df_drop = df_male_full[df_male_full['PARTS1YR']>df_male_full['LIFPRTNR']]
df_male_full = df_male_full.drop(df_drop.index)
df_male_full['INTVWYEAR'] = df_male_full['INTVWYEAR'].astype('int64')

df_female_full['AGE_R'] = df_female_full['AGE_R'].astype('int64')
df_female_full['LIFPRTNR'] = df_female_full['LIFPRTNR'].astype('int64')
df_female_full_virgins = df_female_full[df_female_full['LIFPRTNR']==0]
df_female_full.loc[df_female_full_virgins.index,'PARTS1YR'] = 0
df_female_full['PARTS1YR'] = df_female_full['PARTS1YR'].astype('int64')
df_drop = df_female_full[df_female_full['PARTS1YR']>df_female_full['LIFPRTNR']]
df_female_full = df_female_full.drop(df_drop.index)
df_female_full['INTVWYEAR'] = df_female_full['INTVWYEAR'].astype('int64')

    
#%%filter by age and never married
minage = 23
maxage = 35

df_male_agerange = df_male_full[(df_male_full['AGE_R']<=maxage) & (df_male_full['AGE_R']>=minage) & (df_male_full['MARSTAT']==6)]

df_female_agerange = df_female_full[(df_female_full['AGE_R']<=maxage) & (df_female_full['AGE_R']>=minage) & (df_female_full['MARSTAT']==6)]

df_agerange = {}
df_agerange['male'] = df_male_agerange
df_agerange['female'] = df_female_agerange

#%%num partners by year

percentiles = [5,10,15,20,25,50,75,80,85,90,95]
percentiles = [x/100 for x in percentiles]

years = sorted(list(df_male_agerange['INTVWYEAR'].unique()))

splitvars = ['INTACT18','HAVEDEG']
splitvals = {}
splitvals['INTACT18'] = {'intact home':[1],'broken home':[2]}
splitvals['HAVEDEG'] = {'yes':[1],'no':[5]}

sexes = ['male','female']
targetvars = ['LIFPRTNR','PARTS1YR']

summaries = {}
for sex in sexes:
    summaries[sex] = {}
    for var in targetvars:
        summaries[sex][var] = {}
        summaries[sex][var]['all'] = pd.DataFrame(index=years,columns=percentiles)
        for splitvar in splitvars:
            summaries[sex][var][splitvar] = {}
            for val in splitvals[splitvar].keys():
                summaries[sex][var][splitvar][val] = pd.DataFrame(index=years,columns=percentiles)

for sex in sexes:
    df = df_agerange[sex]
    for year in years:
        df_year = df[df['INTVWYEAR']==year]
        if len(df_year):
            for var in targetvars:
                summaries[sex][var]['all'].loc[year,percentiles] = df_year.quantile(percentiles)[var]
                summaries[sex][var]['all'].loc[year,"N"] = len(df_year)
                summaries[sex][var]['all'].loc[year,"% 0"] = len(df_year[df_year[var]==0])/len(df_year)
                for splitvar in splitvars:
                    for val in splitvals[splitvar].keys():
                        filtervals = splitvals[splitvar][val]
                        df_year_split = df_year[df_year[splitvar].isin(filtervals)]
                        #if len(df_year_split):
                        summaries[sex][var][splitvar][val].loc[year,percentiles] = df_year_split.quantile(percentiles)[var]
                        summaries[sex][var][splitvar][val].loc[year,"N"] = len(df_year_split)
                        summaries[sex][var][splitvar][val].loc[year,"% 0"] = len(df_year_split[df_year_split[var]==0])/len(df_year_split)
                        
#%%Create plots

#no sex - past year
nosex_df = pd.DataFrame(columns = ['male','female'])
nosex_df['male']=summaries['male']['PARTS1YR']['all']['% 0']
nosex_df['female']=summaries['female']['PARTS1YR']['all']['% 0']
nosex_df.plot()

#successful - lifetime partners
success_df = pd.DataFrame(columns = ['90th %le male','90th %le female','75th %le male','75th %le female'])
success_df['90th %le male']=summaries['male']['LIFPRTNR']['all'][0.90]
success_df['90th %le female']=summaries['female']['LIFPRTNR']['all'][0.90]
success_df['75th %le male']=summaries['male']['LIFPRTNR']['all'][0.75]
success_df['75th %le female']=summaries['female']['LIFPRTNR']['all'][0.75]
success_df.plot()

#%%Create plots - with degree
'''
#no sex - past year
nosex_df = pd.DataFrame(columns = ['male','female'])
nosex_df['male']=summaries['male']['PARTS1YR']['HAVEDEG']['yes']['% 0']
nosex_df['female']=summaries['female']['PARTS1YR']['HAVEDEG']['yes']['% 0']
nosex_df.plot()

#successful - lifetime partners
success_df = pd.DataFrame(columns = ['95th %le male','95th %le female','80th %le male','80th %le female'])
success_df['95th %le male']=summaries['male']['LIFPRTNR']['HAVEDEG']['yes'][0.95]
success_df['95th %le female']=summaries['female']['LIFPRTNR']['HAVEDEG']['yes'][0.95]
success_df['80th %le male']=summaries['male']['LIFPRTNR']['HAVEDEG']['yes'][0.8]
success_df['80th %le female']=summaries['female']['LIFPRTNR']['HAVEDEG']['yes'][0.8]
success_df.plot()

#%%Create plots - intact

#intact or not - lifetime partners
success_df = pd.DataFrame(columns = ['80th %le male intact','80th %le female intact','80th %le male not intact','80th %le female not intact'])
success_df['80th %le male intact']=summaries['male']['LIFPRTNR']['INTACT18']['intact home'][0.9]
success_df['80th %le female intact']=summaries['female']['LIFPRTNR']['INTACT18']['intact home'][0.9]
success_df['80th %le male not intact']=summaries['male']['LIFPRTNR']['INTACT18']['broken home'][0.9]
success_df['80th %le female not intact']=summaries['female']['LIFPRTNR']['INTACT18']['broken home'][0.9]
success_df.plot()
'''

#%%save data















