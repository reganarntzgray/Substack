#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\NSFH') 

#%%Imports
import pandas as pd
import numpy as np
import scipy.stats as stats 

#%%Load variables to pull for each wave

varinfo1 = pd.read_excel('variables - divorce.xlsx',sheet_name='wave 1')
varinfo2 = pd.read_excel('variables - divorce.xlsx',sheet_name='wave 2')

#%%read in datasets

datasets1 = list(set(varinfo1['Dataset']))
datasets2 = list(set(varinfo2['Dataset']))

dataset_dict = {}

prepend = varinfo1['prepend'][0]
for dataset in datasets1:
    datasetnum = dataset.replace('DS','')
    dataset_dict[f'wave1_{dataset}'] = pd.read_csv(f'data downloads/NSFH wave 1/{dataset}/0{prepend}-{datasetnum}-Data.tsv', sep='\t', index_col=0)
    
prepend = varinfo2['prepend'][0]
for dataset in datasets2:
    datasetnum = dataset.replace('DS','')
    dataset_dict[f'wave2_{dataset}'] = pd.read_csv(f'data downloads/NSFH wave 2/{dataset}/0{prepend}-{datasetnum}-Data.tsv', sep='\t', index_col=1)
    
#%%gather variables of interest

dataset1 = pd.DataFrame()
for var in varinfo1.index:
    dataset = varinfo1.loc[var,'Dataset']
    dataset1[varinfo1.loc[var,'Text']] = dataset_dict[f'wave1_{dataset}'][varinfo1.loc[var,'Code']]

dataset2 = pd.DataFrame()
for var in varinfo2.index:
    dataset = varinfo2.loc[var,'Dataset']
    dataset2[varinfo2.loc[var,'Text']] = dataset_dict[f'wave2_{dataset}'][varinfo2.loc[var,'Code']]

#%%determine which respondents to keep from both surveys

respondents_w_ex = dataset_dict['wave2_DS0003'].index
married_respondents = dataset1[dataset1['Marital Status of Respondent']==1].index
divorced_respondents = dataset2[dataset2['Marital Status of Respondent']==3].index
divorced_exes = dataset2[dataset2['Marital Status of Respondent-Sec']==3].index
separated_respondents = dataset2[dataset2['Marital Status of Respondent']==2].index
separated_exes = dataset2[dataset2['Marital Status of Respondent-Sec']==2].index
remarried_respondents = dataset2[dataset2['Times married since last interview?']==1].index
remarried_exes = dataset2[dataset2['Times married since last interview?-Sec']==1].index


married_now_divorced = list(set(respondents_w_ex) & set(married_respondents) & set(divorced_respondents))
married_now_divorced_exes = list(set(respondents_w_ex) & set(married_respondents) & set(divorced_exes))

married_now_separated = list(set(respondents_w_ex) & set(married_respondents) & set(separated_respondents))
married_now_separated_exes = list(set(respondents_w_ex) & set(married_respondents) & set(separated_exes))

married_now_remarried = list(set(respondents_w_ex) & set(remarried_respondents) & set(married_respondents))
married_now_remarried_exes = list(set(respondents_w_ex) & set(remarried_exes) & set(married_respondents))

#%%compare happiness before and after separation

happiness = pd.DataFrame(index=['Separated (before)','Separated (after)','Separated (num)','Separated - pval less happiness','Divorced (before)','Divorced (after)','Divorced (num)','Divorced - pval less happiness','Remarried (before)','Remarried (after)','Remarried (num)','Remarried - pval greater happiness'],columns=['Men','Women'])

for respondents,exes,resp_type,alt in zip([married_now_separated, married_now_divorced, married_now_remarried],[married_now_separated_exes, married_now_divorced_exes, married_now_remarried_exes],['Separated','Divorced','Remarried'],['less','less','greater']):
    
    dataset1_sub = dataset1.loc[list(set(respondents))]
    dataset2_sub = dataset2.loc[list(set(respondents))]
    dataset1_sub_exes = dataset1.loc[list(set(exes))]
    dataset2_sub_exes = dataset2.loc[list(set(exes))]

    howarethings1 = dataset1_sub[dataset1_sub['Taking all things together how would you say things are these days?']<=7]
    howarethings2 = dataset2_sub.loc[howarethings1.index]
    howarethings2 = howarethings2[howarethings2['How are things these days?']<=7]
    howarethings1 = howarethings1.loc[howarethings2.index]
    
    howarethings1sec = dataset1_sub_exes[dataset1_sub_exes['Taking all things together how would you say things are these days?-Sec']<=7]
    howarethings2sec = dataset2_sub_exes.loc[howarethings1sec.index]
    howarethings2sec = howarethings2sec[howarethings2sec['How are things these days?-Sec']<=7]
    howarethings1sec = howarethings1sec.loc[howarethings2sec.index]
    
    before_women = howarethings1[howarethings1['Sex of respondent']==2]['Taking all things together how would you say things are these days?']
    before_men = howarethings1[howarethings1['Sex of respondent']==1]['Taking all things together how would you say things are these days?']
    before_women_sec = howarethings1sec[howarethings1sec['Sex of respondent']==1]['Taking all things together how would you say things are these days?-Sec']
    before_men_sec = howarethings1sec[howarethings1sec['Sex of respondent']==2]['Taking all things together how would you say things are these days?-Sec']
    
    before_women_full = pd.concat([before_women,before_women_sec])
    before_men_full = pd.concat([before_men,before_men_sec])
    
    after_women = howarethings2.loc[before_women.index,'How are things these days?']
    after_men = howarethings2.loc[before_men.index,'How are things these days?']
    after_women_sec = howarethings2sec.loc[before_women_sec.index,'How are things these days?-Sec']
    after_men_sec = howarethings2sec.loc[before_men_sec.index,'How are things these days?-Sec']
    
    after_women_full = pd.concat([after_women,after_women_sec])
    after_men_full = pd.concat([after_men,after_men_sec])
    
    happiness.loc[f'{resp_type} (before)','Women'] = before_women_full.mean()
    happiness.loc[f'{resp_type} (before)','Men'] = before_men_full.mean()
    happiness.loc[f'{resp_type} (after)','Women'] = after_women_full.mean()
    happiness.loc[f'{resp_type} (after)','Men'] = after_men_full.mean()
    
    happiness.loc[f'{resp_type} (num)','Women'] = len(before_women_full)
    happiness.loc[f'{resp_type} (num)','Men'] = len(before_men_full)
    
    happiness.loc[f'{resp_type} - pval {alt} happiness','Women'] = stats.ttest_rel(after_women_full, before_women_full, alternative=alt).pvalue
    happiness.loc[f'{resp_type} - pval {alt} happiness','Men'] = stats.ttest_rel(after_men_full, before_men_full, alternative=alt).pvalue
   
#%%Do they feel happier after separating?

comphappiness = pd.DataFrame(index=['Separated','Separated (num)','Divorced','Divorced (num)','Remarried','Remarried (num)'],columns=['Men','Women'])

for respondents,exes,resp_type in zip([married_now_separated, married_now_divorced, married_now_remarried],[married_now_separated_exes, married_now_divorced_exes, married_now_remarried_exes],['Separated','Divorced','Remarried']):
    
    dataset2_sub = dataset2.loc[list(set(respondents))]
    dataset2_sub_exes = dataset2.loc[list(set(exes))]

    howarethings2 = dataset2_sub[dataset2_sub['Overall, how is your life now, compared to the year before you separated?']<=5]
    howarethings1=dataset1.loc[howarethings2.index]
    howarethings1_women = howarethings1[howarethings1['Sex of respondent']==2]
    howarethings1_men = howarethings1[howarethings1['Sex of respondent']==1]
    
    howarethings2sec = dataset2_sub_exes[dataset2_sub_exes['Overall, how is your life now, compared to the year before you separated?-Sec']<=5]
    howarethings1sec=dataset1.loc[howarethings2sec.index]
    howarethings1sec_women = howarethings1sec[howarethings1sec['Sex of respondent']==2]
    howarethings1sec_men = howarethings1sec[howarethings1sec['Sex of respondent']==1]
    
    women = howarethings2.loc[howarethings1_women.index,'Overall, how is your life now, compared to the year before you separated?']
    men = howarethings2.loc[howarethings1_men.index,'Overall, how is your life now, compared to the year before you separated?']
    women_sec = howarethings2sec.loc[howarethings1sec_women.index,'Overall, how is your life now, compared to the year before you separated?-Sec']
    men_sec = howarethings2sec.loc[howarethings1sec_men.index,'Overall, how is your life now, compared to the year before you separated?-Sec']
    
    women_full = pd.concat([women,women_sec])
    men_full = pd.concat([men,men_sec])
    
    comphappiness.loc[f'{resp_type}','Women'] = women_full.mean()
    comphappiness.loc[f'{resp_type}','Men'] = men_full.mean()
    
    comphappiness.loc[f'{resp_type} (num)','Women'] = len(women_full)
    comphappiness.loc[f'{resp_type} (num)','Men'] = len(men_full)
    
#%%export results

writer=pd.ExcelWriter('Happiness after Divorce.xlsx')
happiness.to_excel(writer,sheet_name='overall happiness - 2 points')
comphappiness.to_excel(writer,sheet_name='happiness relative to pre separation')

writer.save()
writer.close()