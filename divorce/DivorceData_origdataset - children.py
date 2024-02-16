#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\Divorce') 

#%%Imports
import pandas as pd
import numpy as np

#%%Load HCMST data
df = pd.read_csv('csv datasets/HCMST - 2009-2015 - w waves.csv')
varnames = pd.read_excel('select variables/HCMST - variables of interest - children - 2009-2015.xlsx')

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

#%%add children under 13 variables for each wave

filter_col = [col for col in sub_df if col.startswith('children')]

sub_df[filter_col] = sub_df[filter_col].fillna(0)

for wave in [1,2,3,4,5]:
    sub_df[f'children under 13 wave {wave}'] = sub_df[f'children 0 to 1 wave {wave}']+sub_df[f'children 2 to 5 wave {wave}']+sub_df[f'children 6 to 12 wave {wave}']

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

breakup_df_all = breakup_df.copy()

#%%filter for kids
kid_dict = dict()
nokid_dict = dict()
for wave in [2,3,4,5]:
    if wave>2:
        kid_dict[wave] = breakup_df_all[((breakup_df_all[f'children under 13 wave {wave-1}']+breakup_df_all[f'children under 13 wave {wave}'])>0) & (breakup_df_all[f'who broke up wave {wave}']>0) & (breakup_df_all[f'who broke up wave {wave-1}']==0)]
        
        nokid_dict[wave] = breakup_df_all[(breakup_df_all[f'children under 13 wave {wave-1}']==0) & (breakup_df_all[f'children under 13 wave {wave}']==0) & (breakup_df_all[f'who broke up wave {wave}']>0) & (breakup_df_all[f'who broke up wave {wave-1}']==0)]
    else:
        kid_dict[wave] = breakup_df_all[((breakup_df_all[f'children under 13 wave {wave-1}']+breakup_df_all[f'children under 13 wave {wave}'])>0) & (breakup_df_all[f'who broke up wave {wave}']>0)]
        
        nokid_dict[wave] = breakup_df_all[(breakup_df_all[f'children under 13 wave {wave-1}']==0) & (breakup_df_all[f'children under 13 wave {wave}']==0) & (breakup_df_all[f'who broke up wave {wave}']>0)]

breakup_df_kids = pd.concat([kid_dict[2],kid_dict[3],kid_dict[4],kid_dict[5]])

breakup_df_nokids = pd.concat([nokid_dict[2],nokid_dict[3],nokid_dict[4],nokid_dict[5]])

#%%create all, kids and no kids versions of hetero_married_df

hetero_married_df_all = hetero_married_df.copy()

hetero_married_df_kids = hetero_married_df[(hetero_married_df['children under 13 wave 1']>0) | (hetero_married_df['children under 13 wave 2']>0) | (hetero_married_df['children under 13 wave 3']>0) | (hetero_married_df['children under 13 wave 4']>0) | (hetero_married_df['children under 13 wave 5']>0)]

hetero_married_df_nokids = hetero_married_df[(hetero_married_df['children under 13 wave 1']==0) & (hetero_married_df['children under 13 wave 2']==0) & (hetero_married_df['children under 13 wave 3']==0) & (hetero_married_df['children under 13 wave 4']==0) & (hetero_married_df['children under 13 wave 5']==0)]

#%%compare chance of divorce and who initiates in various circumstances

writer = pd.ExcelWriter('summaries/HCMST - hetero marriage break up analysis - with or without kids - 2009-2015.xlsx')
for breakup_df, hetero_married_df ,dfname in zip([breakup_df_all, breakup_df_kids, breakup_df_nokids], [hetero_married_df_all, hetero_married_df_kids, hetero_married_df_nokids], ['all','kids','no kids']):

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
    
    #%%filter for woman makes less
    
    woman_makes_less_breakup_df = breakup_df.loc[(breakup_df['gender']==2) & (breakup_df['who earned more'] == 3) | (breakup_df['gender']==1) & (breakup_df['who earned more'] == 1)]
    
    woman_makes_less_df = hetero_married_df.loc[(hetero_married_df['gender']==2) & (hetero_married_df['who earned more'] == 3) | (hetero_married_df['gender']==1) & (hetero_married_df['who earned more'] == 1)]
    
    #%%filter for woman makes same
    
    woman_makes_same_breakup_df = breakup_df.loc[breakup_df['who earned more'] == 2]
    
    woman_makes_same_df = hetero_married_df.loc[hetero_married_df['who earned more'] == 2]
    
    #%%summarize data
    
    rows = ['all hetero marriages','wife has a degree','wife more educated','wife has a degree, husband does not','wife makes more','wife makes same','wife makes less']
    columns = ['# obs','# breakups','avg. relationship quality (all)','avg. relationship quality (breakups)','prob. of breakup','% of breakups initiated by woman','% of breakups initiated by woman only','% of breakups initiated by man only','% of breakups initiated by both','avg. hh income (all)', 'avg. hh income (breakups)']
    
    summary_df = pd.DataFrame(index=rows,columns=columns)
    
    for (row, df_break, df_full) in zip(rows,[breakup_df, woman_has_degree_breakup_df, woman_more_ed_breakup_df, woman_has_degree_man_doesnt_breakup_df, woman_makes_more_breakup_df, woman_makes_same_breakup_df, woman_makes_less_breakup_df],[hetero_married_df, woman_has_degree_df, woman_more_ed_df, woman_has_degree_man_doesnt_df, woman_makes_more_df, woman_makes_same_df, woman_makes_less_df]):
        summary_df.loc[row,'# obs'] = len(df_full)
        summary_df.loc[row,'# breakups'] = len(df_break)
        summary_df.loc[row,'avg. relationship quality (all)'] = df_full['relationship quality'].mean()
        summary_df.loc[row,'avg. relationship quality (breakups)'] = df_break['relationship quality'].mean()
        summary_df.loc[row,'prob. of breakup'] = len(df_break)/len(df_full)
        summary_df.loc[row,'% of breakups initiated by woman'] = df_break['woman broke up'].mean()
        womanonly = df_break[df_break['woman broke up']==1]
        manonly = df_break[df_break['woman broke up']==0]
        both = df_break[df_break['woman broke up']==0.5]
        
        summary_df.loc[row,'% of breakups initiated by woman only'] = len(womanonly)/len(df_break)
        summary_df.loc[row,'% of breakups initiated by man only'] = len(manonly)/len(df_break)
        summary_df.loc[row,'% of breakups initiated by both'] = len(both)/len(df_break)
        
        summary_df.loc[row,'avg. hh income (all)'] = df_full['hh income wave 1'].mean()
        summary_df.loc[row,'avg. hh income (breakups)'] = df_break['hh income wave 1'].mean()
    
    summary_df.to_excel(writer,sheet_name=f'summary {dfname}')

sub_df.to_excel(writer,sheet_name='data')

writer.save()
writer.close()



