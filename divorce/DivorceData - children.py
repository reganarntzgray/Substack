#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\Divorce') 

#%%Imports
import pandas as pd
import numpy as np

#%%Load HCMST data
df = pd.read_csv('csv datasets/HCMST - 2017-2022.csv')
varnames = pd.read_excel('select variables/HCMST - variables of interest - children - 2017-2022.xlsx')

#%%select subset of data 
sub_df = df[varnames['variable name']]
sub_df.columns = varnames['description']

#%%add variable for wave 1 children under 13

sub_df['children 0 to 1 wave 1'] = sub_df['children 0 to 1 wave 1'].fillna(0)
sub_df['children 2 to 5 wave 1'] = sub_df['children 2 to 5 wave 1'].fillna(0)
sub_df['children 6 to 12 wave 1'] = sub_df['children 6 to 12 wave 1'].fillna(0)

sub_df['children under 13 wave 1'] = sub_df['children 0 to 1 wave 1']+sub_df['children 2 to 5 wave 1']+sub_df['children 6 to 12 wave 1']

#replace nan values with 0s in "children under 13"
sub_df['children under 13 wave 1'] = sub_df['children under 13 wave 1'].fillna(0)
sub_df['children under 13 wave 2'] = sub_df['children under 13 wave 2'].fillna(0)
sub_df['children under 13 wave 3'] = sub_df['children under 13 wave 3'].fillna(0)


#%%Filter data for married (as of w1) and hetero (genders don't match)

hetero_married_df = sub_df[(sub_df['married']==1) & (sub_df['gender']!=sub_df['partner gender'])]

#%%filter for break ups

breakup_df = hetero_married_df[hetero_married_df['who broke up wave 2'].notna() | hetero_married_df['who broke up wave 3'].notna()]

#add columns for breakup where we only look at wave 3 data if wave 2 is missing (not looking at new breakups in wave 3)
whobrokeup = breakup_df['who broke up wave 2'].copy()
whobrokeup[whobrokeup.isnull()]=breakup_df[whobrokeup.isnull()]['who broke up wave 3']

womanbrokeup = breakup_df['women wanted breakup wave 2'].copy()
womanbrokeup[womanbrokeup.isnull()]=breakup_df[womanbrokeup.isnull()]['women wanted breakup wave 3']

breakup_df['who broke up'] = whobrokeup
breakup_df['woman broke up'] = womanbrokeup

breakup_df_all = breakup_df.copy()

#%%filter for children under 13 (waves 1, 2 and 3) equal to 0

break_w2_with_kids = breakup_df_all[((breakup_df_all['children under 13 wave 1']+breakup_df_all['children under 13 wave 2'])>0) & (breakup_df_all['who broke up wave 2'].notna())]

break_w2_no_kids = breakup_df_all[(breakup_df_all['children under 13 wave 1']==0) & (breakup_df_all['children under 13 wave 2']==0) & (breakup_df_all['who broke up wave 2'].notna())]

break_w2 = breakup_df_all[(breakup_df_all['who broke up wave 2'].notna())]

break_w3_with_kids = breakup_df_all[((breakup_df_all['children under 13 wave 2']+ breakup_df_all['children under 13 wave 3'])>0) & (breakup_df_all['who broke up wave 2'].isna())]

break_w3_no_kids = breakup_df_all[(breakup_df_all['children under 13 wave 2']==0) & (breakup_df_all['children under 13 wave 3']==0) & (breakup_df_all['who broke up wave 2'].isna())]

break_w3 = breakup_df_all[(breakup_df_all['who broke up wave 2'].isna())]

breakup_df_kids = pd.concat([break_w2_with_kids,break_w3_with_kids])

breakup_df_nokids = pd.concat([break_w2_no_kids,break_w3_no_kids])

#%%create all, kids and no kids versions of hetero_married_df

hetero_married_df_all = hetero_married_df.copy()

hetero_married_df_kids = hetero_married_df[(hetero_married_df['children under 13 wave 1']>0) | (hetero_married_df['children under 13 wave 2']>0) | (hetero_married_df['children under 13 wave 3']>0)]

hetero_married_df_nokids = hetero_married_df[(hetero_married_df['children under 13 wave 1']==0) & (hetero_married_df['children under 13 wave 2']==0) & (hetero_married_df['children under 13 wave 3']==0)]


#%%compare chance of divorce and who initiates in various circumstances

writer = pd.ExcelWriter('summaries/HCMST - hetero marriage break up analysis - with or without kids - 2017-2022.xlsx')
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



