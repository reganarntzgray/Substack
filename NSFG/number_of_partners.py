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

    
#%%filter by age
minage = 18
maxage = 22

df_male_agerange = df_male_full[(df_male_full['AGE_R']<=maxage) & (df_male_full['AGE_R']>=minage)]

df_female_agerange = df_female_full[(df_female_full['AGE_R']<=maxage) & (df_female_full['AGE_R']>=minage)]

df_agerange = {}
df_agerange['male'] = df_male_agerange
df_agerange['female'] = df_female_agerange

#%%num partners by year

percentiles = [5,10,15,20,25,50,75,80,85,90,95]
percentiles = [x/100 for x in percentiles]

years = sorted(list(df_male_agerange['INTVWYEAR'].unique()))

splitvars = ['INTACT18','MARSTAT','HAVEDEG']
splitvals = {}
splitvals['INTACT18'] = {'intact home':[1],'broken home':[2]}
splitvals['MARSTAT'] = {'never married':[6],'married/cohabitating':[1,2],'divorced/separated/widowed':[3,4,5]}
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
                        if (splitvar=='MARSTAT' and val=='married/cohabitating'):
                            summaries[sex][var]['all'].loc[year,"% married/cohabitating"] =len(df_year_split)/len(df_year)
                        if len(df_year_split):
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
success_df['90th %le male']=summaries['male']['LIFPRTNR']['all'][0.9]
success_df['90th %le female']=summaries['female']['LIFPRTNR']['all'][0.9]
success_df['75th %le male']=summaries['male']['LIFPRTNR']['all'][0.75]
success_df['75th %le female']=summaries['female']['LIFPRTNR']['all'][0.75]
success_df.plot()

#%married/cohabitating
marriedpct = pd.DataFrame(columns = ['male','female'])
marriedpct['female'] = summaries['female']['LIFPRTNR']['all']['% married/cohabitating']
marriedpct['male'] = summaries['male']['LIFPRTNR']['all']['% married/cohabitating']
marriedpct.plot()

#never married versions
nosex_df_nevermarried = pd.DataFrame(columns = ['male','female'])
nosex_df_nevermarried['male']=summaries['male']['PARTS1YR']['MARSTAT']['never married']['% 0']
nosex_df_nevermarried['female']=summaries['female']['PARTS1YR']['MARSTAT']['never married']['% 0']
nosex_df_nevermarried.plot()

#successful - lifetime partners
success_df_nevermarried = pd.DataFrame(columns = ['90th %le male','90th %le female','75th %le male','75th %le female'])
success_df_nevermarried['90th %le male']=summaries['male']['LIFPRTNR']['MARSTAT']['never married'][0.9]
success_df_nevermarried['90th %le female']=summaries['female']['LIFPRTNR']['MARSTAT']['never married'][0.9]
success_df_nevermarried['75th %le male']=summaries['male']['LIFPRTNR']['MARSTAT']['never married'][0.75]
success_df_nevermarried['75th %le female']=summaries['female']['LIFPRTNR']['MARSTAT']['never married'][0.75]
success_df_nevermarried.plot()

#%%save data

writer = pd.ExcelWriter(f'output/number of partners {minage} to {maxage}.xlsx')
summaries['male']['LIFPRTNR']['all'].to_excel(writer,sheet_name='num lifetime prtnrs - male')
summaries['female']['LIFPRTNR']['all'].to_excel(writer,sheet_name='num lifetime prtnrs - female')
summaries['male']['PARTS1YR']['all'].to_excel(writer,sheet_name='num prtnrs 1yr - male')
summaries['female']['PARTS1YR']['all'].to_excel(writer,sheet_name='num prtnrs 1yr - female')
nosex_df.to_excel(writer,sheet_name='no sex 1yr')
success_df.to_excel(writer,sheet_name='lifetime prtnrs - successful')
marriedpct.to_excel(writer,sheet_name='% married or cohabitating')

writer.save()
writer.close()

writer = pd.ExcelWriter(f'output/number of partners {minage} to {maxage} - never married.xlsx')
summaries['male']['LIFPRTNR']['MARSTAT']['never married'].to_excel(writer,sheet_name='num lifetime prtnrs - male')
summaries['female']['LIFPRTNR']['MARSTAT']['never married'].to_excel(writer,sheet_name='num lifetime prtnrs - female')
summaries['male']['PARTS1YR']['MARSTAT']['never married'].to_excel(writer,sheet_name='num prtnrs 1yr - male')
summaries['female']['PARTS1YR']['MARSTAT']['never married'].to_excel(writer,sheet_name='num prtnrs 1yr - female')
nosex_df_nevermarried.to_excel(writer,sheet_name='no sex 1yr')
success_df_nevermarried.to_excel(writer,sheet_name='lifetime prtnrs - successful')

writer.save()
writer.close()















