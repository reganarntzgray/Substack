#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\political affiliation') 

#%%Imports 
import pandas as pd
import matplotlib.pyplot as plt

#%%read in data

file = 'GSS data.xlsx'
df_gss = pd.read_excel(file, sheet_name='Data')
varnames = pd.read_excel(file, sheet_name='Variables', index_col=0)

varnames_dict = varnames['label'].to_dict()
df_gss.rename(columns=varnames_dict, inplace=True)

#name output file
output = 'GSS data summary.xlsx'
writer = pd.ExcelWriter(output)

#%%Political affiliation - age < 30
df_gss_older = df_gss[df_gss['age of respondent'].str.contains('older')]
df_gss.loc[df_gss_older.index,'age of respondent'] = '89'
df_gss_noage = df_gss[df_gss['age of respondent'].str.contains(':')]

df_gss_wage = df_gss.drop(df_gss_noage.index)

df_gss_wage['age of respondent'] = df_gss_wage['age of respondent'].astype('int64')

#filter df_gss for age < 30
max_age = 30
df_gss_under30 = df_gss_wage[df_gss_wage['age of respondent']<max_age]

#%%%version 1 - based on party

#lumping party affiliation into republican or democrat
df_gss_under30_noparty = df_gss_under30[df_gss_under30['political party affiliation'].str.contains(':')]
df_gss_under30_wparty = df_gss_under30.drop(df_gss_under30_noparty.index)

political_party_dict = {'Independent, close to democrat':'Dem','Not very strong democrat':'Dem', 'Independent (neither, no response)':'Ind', 'Strong democrat':'Dem', 'Not very strong republican':'Rep','Independent, close to republican':'Rep','Strong republican':'Rep','Other party':'Other'}

df_gss_under30_wparty['Lumped Party'] = df_gss_under30_wparty['political party affiliation'].map(political_party_dict)

df_gss_under30_wparty_f = df_gss_under30_wparty[df_gss_under30_wparty['respondents sex']=='FEMALE']
df_gss_under30_wparty_m = df_gss_under30_wparty[df_gss_under30_wparty['respondents sex']=='MALE']

#counting each reply for females and males by year
years = list(df_gss_under30_wparty['GSS year for this respondent'].unique())
cols = list(df_gss_under30_wparty['Lumped Party'].unique())
df_summary_f = pd.DataFrame(index=years,columns=cols)
df_summary_m = pd.DataFrame(index=years,columns=cols)

for year in years:
    for col in cols:
        for df, df_sum in zip([df_gss_under30_wparty_f,df_gss_under30_wparty_m],[df_summary_f,df_summary_m]):
            df_filtered = df[df['GSS year for this respondent']==year]
            df_filtered = df_filtered[df_filtered['Lumped Party']==col]
            df_sum.loc[year,col] = len(df_filtered)  

for df_sum in [df_summary_f,df_summary_m]:
    obs = df_sum.sum(axis=1)
    df_sum['% Dem'] = df_sum['Dem']/obs
    df_sum['% Rep'] = df_sum['Rep']/obs
    df_sum['% Dem - % Rep'] = df_sum['% Dem']-df_sum['% Rep']
    df_sum['obs'] = obs

df_plot=pd.concat([df_summary_f['% Dem - % Rep'],df_summary_m['% Dem - % Rep']], axis=1)
df_plot.columns = ['Female','Male']

#plot results
plt.plot(df_plot)    

df_summary_f.to_excel(writer,sheet_name='under 30 - lumped by party - f')
df_summary_m.to_excel(writer,sheet_name='under 30 - lumped by party - m')
df_plot.to_excel(writer, sheet_name='under 30 - lumped party - plot')

#looking at strong rep and strong dem trends

#counting each reply for females and males by year
years = list(df_gss_under30_wparty['GSS year for this respondent'].unique())
cols = list(df_gss_under30_wparty['political party affiliation'].unique())
df_summary_f = pd.DataFrame(index=years,columns=cols)
df_summary_m = pd.DataFrame(index=years,columns=cols)

for year in years:
    for col in cols:
        for df, df_sum in zip([df_gss_under30_wparty_f,df_gss_under30_wparty_m],[df_summary_f,df_summary_m]):
            df_filtered = df[df['GSS year for this respondent']==year]
            df_filtered = df_filtered[df_filtered['political party affiliation']==col]
            df_sum.loc[year,col] = len(df_filtered)  

for df_sum in [df_summary_f,df_summary_m]:
    obs = df_sum.sum(axis=1)
    df_sum['% Strong Dem'] = df_sum['Strong democrat']/obs
    df_sum['% Strong Rep'] = df_sum['Strong republican']/obs
    df_sum['% Strong Dem - % Strong Rep'] = df_sum['% Strong Dem']-df_sum['% Strong Rep']
    df_sum['obs'] = obs

df_plot=pd.concat([df_summary_f['% Strong Dem - % Strong Rep'],df_summary_m['% Strong Dem - % Strong Rep']], axis=1)
df_plot.columns = ['Female','Male']

#plot results
plt.plot(df_plot) 

df_summary_f.to_excel(writer,sheet_name='under 30 - strong by party - f')
df_summary_m.to_excel(writer,sheet_name='under 30 - strong by party - m')
df_plot.to_excel(writer, sheet_name='under 30 - strong party - plot')

#%%%version 2 - based on think of self

#lumping think of self into conservative or liberal
df_gss_under30_nothink = df_gss_under30[df_gss_under30['think of self as liberal or conservative'].str.contains(':')]
df_gss_under30_wthink = df_gss_under30.drop(df_gss_under30_nothink.index)

think_of_self_dict = {'Slightly liberal':'Lib','Liberal':'Lib', 'Extremely liberal':'Lib', 'Slightly conservative':'Con','Conservative':'Con', 'Extremely conservative':'Con','Moderate, middle of the road':'Mod'}

df_gss_under30_wthink['Lumped think'] = df_gss_under30_wthink['think of self as liberal or conservative'].map(think_of_self_dict)

df_gss_under30_wthink_f = df_gss_under30_wthink[df_gss_under30_wthink['respondents sex']=='FEMALE']
df_gss_under30_wthink_m = df_gss_under30_wthink[df_gss_under30_wthink['respondents sex']=='MALE']

#counting each reply for females and males by year
years = list(df_gss_under30_wthink['GSS year for this respondent'].unique())
cols = list(df_gss_under30_wthink['Lumped think'].unique())
df_summary_f = pd.DataFrame(index=years,columns=cols)
df_summary_m = pd.DataFrame(index=years,columns=cols)

for year in years:
    for col in cols:
        for df, df_sum in zip([df_gss_under30_wthink_f,df_gss_under30_wthink_m],[df_summary_f,df_summary_m]):
            df_filtered = df[df['GSS year for this respondent']==year]
            df_filtered = df_filtered[df_filtered['Lumped think']==col]
            df_sum.loc[year,col] = len(df_filtered)  

for df_sum in [df_summary_f,df_summary_m]:
    obs = df_sum.sum(axis=1)
    df_sum['% Lib'] = df_sum['Lib']/obs
    df_sum['% Con'] = df_sum['Con']/obs
    df_sum['% Lib - % Con'] = df_sum['% Lib']-df_sum['% Con']
    df_sum['obs'] = obs

df_plot=pd.concat([df_summary_f['% Lib - % Con'],df_summary_m['% Lib - % Con']], axis=1)
df_plot.columns = ['Female','Male']

#plot results
plt.plot(df_plot)    

df_summary_f.to_excel(writer,sheet_name='under 30 - lumped by think- f')
df_summary_m.to_excel(writer,sheet_name='under 30 - lumped by think - m')
df_plot.to_excel(writer, sheet_name='under 30 - lumped think - plot')

#looking at strong rep and strong dem trends

#counting each reply for females and males by year
years = list(df_gss_under30_wparty['GSS year for this respondent'].unique())
cols = list(df_gss_under30_wparty['think of self as liberal or conservative'].unique())
df_summary_f = pd.DataFrame(index=years,columns=cols)
df_summary_m = pd.DataFrame(index=years,columns=cols)

for year in years:
    for col in cols:
        for df, df_sum in zip([df_gss_under30_wparty_f,df_gss_under30_wparty_m],[df_summary_f,df_summary_m]):
            df_filtered = df[df['GSS year for this respondent']==year]
            df_filtered = df_filtered[df_filtered['think of self as liberal or conservative']==col]
            df_sum.loc[year,col] = len(df_filtered)  

for df_sum in [df_summary_f,df_summary_m]:
    obs = df_sum.sum(axis=1)
    df_sum['% Extreme Lib'] = df_sum['Extremely liberal']/obs
    df_sum['% Extreme Con'] = df_sum['Extremely conservative']/obs
    df_sum['% Extreme Lib - % Extreme Con'] = df_sum['% Extreme Lib']-df_sum['% Extreme Con']
    df_sum['obs'] = obs
    

df_plot=pd.concat([df_summary_f['% Extreme Lib - % Extreme Con'],df_summary_m['% Extreme Lib - % Extreme Con']], axis=1)
df_plot.columns = ['Female','Male']

#plot results
plt.plot(df_plot) 

df_summary_f.to_excel(writer,sheet_name='under 30 - extreme think - f')
df_summary_m.to_excel(writer,sheet_name='under 30 - extreme think - m')
df_plot.to_excel(writer, sheet_name='under 30 - extreme think - plot')

#%% For or against the preferential hiring of women by sex over time

df_no_pref = df_gss_wage[df_gss_wage['for or against preferential hiring of women'].str.contains(':')]
df_pref_hiring = df_gss_wage.drop(df_no_pref.index)

fororagainst_dict = {'Not strongly oppose':'Oppose','Strongly oppose':'Oppose','Not strongly favor':'Favor','Strongly favor':'Favor'}

df_pref_hiring['Lumped Opinion'] = df_pref_hiring['for or against preferential hiring of women'].map(fororagainst_dict)

df_pref_hiring_under30 = df_pref_hiring[df_pref_hiring['age of respondent']<30]

df_pref_hiring_under30_f = df_pref_hiring_under30[df_pref_hiring_under30['respondents sex']=='FEMALE']
df_pref_hiring_under30_m = df_pref_hiring_under30[df_pref_hiring_under30['respondents sex']=='MALE']

#counting each reply for females and males by year
years = list(df_pref_hiring_under30['GSS year for this respondent'].unique())
cols = list(df_pref_hiring_under30['Lumped Opinion'].unique())
df_summary_f = pd.DataFrame(index=years,columns=cols)
df_summary_m = pd.DataFrame(index=years,columns=cols)

for year in years:
    for col in cols:
        for df, df_sum in zip([df_pref_hiring_under30_f,df_pref_hiring_under30_m],[df_summary_f,df_summary_m]):
            df_filtered = df[df['GSS year for this respondent']==year]
            df_filtered = df_filtered[df_filtered['Lumped Opinion']==col]
            df_sum.loc[year,col] = len(df_filtered)  

for df_sum in [df_summary_f,df_summary_m]:
    obs = df_sum.sum(axis=1)
    df_sum['% Oppose'] = df_sum['Oppose']/obs
    df_sum['% Favor'] = df_sum['Favor']/obs
    df_sum['% Favor - % Oppose'] = df_sum['% Favor']-df_sum['% Oppose']
    df_sum['obs'] = obs
    

df_plot=pd.concat([df_summary_f['% Favor - % Oppose'],df_summary_m['% Favor - % Oppose']], axis=1)
df_plot.columns = ['Female','Male']

#plot results
plt.plot(df_plot)    

df_summary_f.to_excel(writer,sheet_name='under 30 - pref hiring - f')
df_summary_m.to_excel(writer,sheet_name='under 30 - pref hiring - m')
df_plot.to_excel(writer, sheet_name='under 30 - pref hiring - plot')

#by age group and political affiliation currently
### didn't output results - too few obs to be useful ###

df_pref_hiring_nothink = df_pref_hiring[df_pref_hiring['think of self as liberal or conservative'].str.contains(':')]
df_pref_hiring_wthink = df_pref_hiring.drop(df_pref_hiring_nothink.index)

think_of_self_dict = {'Slightly liberal':'Lib','Liberal':'Lib', 'Extremely liberal':'Lib', 'Slightly conservative':'Con','Conservative':'Con', 'Extremely conservative':'Con','Moderate, middle of the road':'Mod'}

df_pref_hiring_wthink['Lumped think'] = df_pref_hiring_wthink['think of self as liberal or conservative'].map(think_of_self_dict)

year = 2022
mins = [18,30,50,65]
maxs = [29,49,64,89]

df_pref_hiring_2022 = df_pref_hiring_wthink[df_pref_hiring_wthink['GSS year for this respondent']==2022]

df_pref_hiring_2022_f = df_pref_hiring_2022[df_pref_hiring_2022['respondents sex']=='FEMALE']
df_pref_hiring_2022_m = df_pref_hiring_2022[df_pref_hiring_2022['respondents sex']=='MALE']

df_summary_f = pd.DataFrame(index=['Lib','Mod','Con'],columns=maxs)
df_summary_m = pd.DataFrame(index=['Lib','Mod','Con'],columns=maxs)

for pol in ['Lib','Mod','Con']:
    for minage,maxage in zip(mins,maxs):
        for df_sum, df in zip([df_summary_f,df_summary_m],[df_pref_hiring_2022_f,df_pref_hiring_2022_m]):
            df_filter = df[df['Lumped think']==pol]
            df_filter = df_filter[df_filter['age of respondent']<=maxage]
            df_filter = df_filter[df_filter['age of respondent']>=minage]
            df_oppose = df_filter[df_filter['Lumped Opinion']=='Oppose']
            df_support = df_filter[df_filter['Lumped Opinion']=='Favor']
            df_sum.loc[pol,maxage] = (len(df_support)-len(df_oppose))/(len(df_support)+len(df_oppose))

df_plot_lib = pd.concat([df_summary_f.loc['Lib'],df_summary_m.loc['Lib']],axis=1)
df_plot_mod = pd.concat([df_summary_f.loc['Mod'],df_summary_m.loc['Mod']],axis=1)
df_plot_con = pd.concat([df_summary_f.loc['Con'],df_summary_m.loc['Con']],axis=1)

plt.plot(df_plot_con)

writer.save()
writer.close()









