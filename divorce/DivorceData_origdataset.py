#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\Divorce') 

#%%Imports
import pandas as pd
import numpy as np

#%%Load HCMST data
df = pd.read_csv('csv datasets/HCMST - 2009-2015 - w waves.csv')
varnames = pd.read_excel('select variables/HCMST - variables of interest - 2009-2015.xlsx')

#%%select subset of data 
sub_df = df[varnames['variable name']]
sub_df.columns = varnames['description']

#%%add women wanted break up wave 2 - 5

sub_df['women wanted breakup wave 2'] = np.nan
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 2']==1)].index
sub_df.loc[rows,'women wanted breakup wave 2'] = 1
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 2']==2)].index
sub_df.loc[rows,'women wanted breakup wave 2'] = 1
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 2']==2)].index
sub_df.loc[rows,'women wanted breakup wave 2'] = 0
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 2']==1)].index
sub_df.loc[rows,'women wanted breakup wave 2'] = 0
rows = sub_df[sub_df['who broke up wave 2']==3].index
sub_df.loc[rows,'women wanted breakup wave 2'] = 0.5


sub_df['women wanted breakup wave 3'] = np.nan
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 3']==1)].index
sub_df.loc[rows,'women wanted breakup wave 3'] = 1
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 3']==2)].index
sub_df.loc[rows,'women wanted breakup wave 3'] = 1
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 3']==2)].index
sub_df.loc[rows,'women wanted breakup wave 3'] = 0
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 3']==1)].index
sub_df.loc[rows,'women wanted breakup wave 3'] = 0
rows = sub_df[sub_df['who broke up wave 3']==3].index
sub_df.loc[rows,'women wanted breakup wave 3'] = 0.5

sub_df['women wanted breakup wave 4'] = np.nan
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 4']==1)].index
sub_df.loc[rows,'women wanted breakup wave 4'] = 1
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 4']==2)].index
sub_df.loc[rows,'women wanted breakup wave 4'] = 1
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 4']==2)].index
sub_df.loc[rows,'women wanted breakup wave 4'] = 0
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 4']==1)].index
sub_df.loc[rows,'women wanted breakup wave 4'] = 0
rows = sub_df[sub_df['who broke up wave 4']==3].index
sub_df.loc[rows,'women wanted breakup wave 4'] = 0.5

sub_df['women wanted breakup wave 5'] = np.nan
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 5']==1)].index
sub_df.loc[rows,'women wanted breakup wave 5'] = 1
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 5']==2)].index
sub_df.loc[rows,'women wanted breakup wave 5'] = 1
rows = sub_df[(sub_df['gender']==2) & (sub_df['who broke up wave 5']==2)].index
sub_df.loc[rows,'women wanted breakup wave 5'] = 0
rows = sub_df[(sub_df['gender']==1) & (sub_df['who broke up wave 5']==1)].index
sub_df.loc[rows,'women wanted breakup wave 5'] = 0
rows = sub_df[sub_df['who broke up wave 5']==3].index
sub_df.loc[rows,'women wanted breakup wave 5'] = 0.5

#%%Filter data for married (as of w1) and hetero (ex same sex or refused responses) - used this because there was a lot of missing partner gender data in this survey

hetero_married_df = sub_df[(sub_df['married']==1) & (sub_df['gender']!=sub_df['partner gender'])]

#fill in missing gender
female_respondents = hetero_married_df[(hetero_married_df['gender']==2)].index
hetero_married_df.loc[female_respondents,'partner gender']=1

male_respondents = hetero_married_df[(hetero_married_df['gender']==1)].index
hetero_married_df.loc[male_respondents,'partner gender']=2

#%%filter for break ups

breakup_df = hetero_married_df[hetero_married_df['women wanted breakup wave 2'].notna() | hetero_married_df['women wanted breakup wave 3'].notna() | hetero_married_df['women wanted breakup wave 4'].notna() | hetero_married_df['women wanted breakup wave 5'].notna()]

#add columns for breakup where we only look at wave 3 data if wave 2 is missing (not looking at new breakups in wave 3)

womanbrokeup = breakup_df['women wanted breakup wave 2']
womanbrokeup[womanbrokeup.isnull()]=breakup_df[womanbrokeup.isnull()]['women wanted breakup wave 3']
womanbrokeup[womanbrokeup.isnull()]=breakup_df[womanbrokeup.isnull()]['women wanted breakup wave 4']
womanbrokeup[womanbrokeup.isnull()]=breakup_df[womanbrokeup.isnull()]['women wanted breakup wave 5']

breakup_df['woman broke up'] = womanbrokeup

#%%filter for woman has more education

woman_more_ed_breakup_df = breakup_df.loc[(breakup_df['gender']==2) & (breakup_df['education'] > breakup_df['partner education']) | (breakup_df['gender']==1) & (breakup_df['education'] < breakup_df['partner education'])]

#filter non breakup df to get denominator in likelihood of divorce
woman_more_ed_df = hetero_married_df.loc[(hetero_married_df['gender']==2) & (hetero_married_df['education'] > hetero_married_df['partner education']) | (hetero_married_df['gender']==1) & (hetero_married_df['education'] < hetero_married_df['partner education'])]

#%%filter for woman has a college degree

woman_has_degree_breakup_df = breakup_df.loc[(breakup_df['gender']==2) & (breakup_df['education'] >= 12) | (breakup_df['gender']==1) & (breakup_df['partner education'] >= 12)]

woman_has_degree_df = hetero_married_df.loc[(hetero_married_df['gender']==2) & (hetero_married_df['education'] >= 12) | (hetero_married_df['gender']==1) & (hetero_married_df['partner education'] >= 12)]

#%%filter for woman has a college degree and man doesn't

woman_has_degree_man_doesnt_breakup_df = breakup_df.loc[(breakup_df['gender']==2) & (breakup_df['education'] >= 12) & (breakup_df['partner education'] < 12) | (breakup_df['gender']==1) & (breakup_df['education'] < 12) & (breakup_df['partner education'] >= 12)]

woman_has_degree_man_doesnt_df = hetero_married_df.loc[(hetero_married_df['gender']==2) & (hetero_married_df['education'] >= 12) & (hetero_married_df['partner education'] < 12) | (hetero_married_df['gender']==1) & (hetero_married_df['education'] < 12) & (hetero_married_df['partner education'] >= 12)]

#%%filter for woman makes more

woman_makes_more_breakup_df = breakup_df.loc[(breakup_df['gender']==2) & (breakup_df['who earned more'] == 1) | (breakup_df['gender']==1) & (breakup_df['who earned more'] == 3)]

woman_makes_more_df = hetero_married_df.loc[(hetero_married_df['gender']==2) & (hetero_married_df['who earned more'] == 1) | (hetero_married_df['gender']==1) & (hetero_married_df['who earned more'] == 3)]

#%%summarize data

rows = ['all hetero marriages','wife has a degree','wife more educated','wife has a degree, husband does not','wife makes more']
columns = ['# obs','# breakups','avg. relationship quality (all)','avg. relationship quality (breakups)','prob. of breakup','% of breakups initiated by woman']

summary_df = pd.DataFrame(index=rows,columns=columns)

for (row, df_break, df_full) in zip(rows,[breakup_df, woman_has_degree_breakup_df, woman_more_ed_breakup_df, woman_has_degree_man_doesnt_breakup_df, woman_makes_more_breakup_df],[hetero_married_df, woman_has_degree_df, woman_more_ed_df, woman_has_degree_man_doesnt_df, woman_makes_more_df]):
    summary_df.loc[row,'# obs'] = len(df_full)
    summary_df.loc[row,'# breakups'] = len(df_break)
    summary_df.loc[row,'avg. relationship quality (all)'] = df_full['relationship quality'].mean()
    summary_df.loc[row,'avg. relationship quality (breakups)'] = df_break['relationship quality'].mean()
    summary_df.loc[row,'prob. of breakup'] = len(df_break)/len(df_full)
    summary_df.loc[row,'% of breakups initiated by woman'] = df_break['woman broke up'].mean()

writer = pd.ExcelWriter('summaries/HCMST - hetero marriage break up analysis - 2009-2015.xlsx')
summary_df.to_excel(writer,sheet_name='summary')
sub_df.to_excel(writer,sheet_name='data')

writer.save()
writer.close()



