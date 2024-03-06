#%%Navigate to folder
import os
os.chdir(r'C:\Users\regan\OneDrive\Documents\Intellectual Projects\Sexual Partners') 

#%%Imports 
import pandas as pd
import matplotlib.pyplot as plt

#%%read in data

file = 'GSS - sexual partners.xlsx'
df_gss = pd.read_excel(file, sheet_name='Data')
varnames = pd.read_excel(file, sheet_name='Variables', index_col=0)

varnames_dict = varnames['label'].to_dict()
df_gss.rename(columns=varnames_dict, inplace=True)

#%%Add lumped political party variable

political_party_dict = {'Independent, close to democrat':'Dem','Not very strong democrat':'Dem', 'Independent (neither, no response)':'Other', 'Strong democrat':'Dem', 'Not very strong republican':'Rep','Independent, close to republican':'Rep','Strong republican':'Rep','Other party':'Other'}

df_gss['Lumped Party'] = df_gss['political party affiliation'].map(political_party_dict)

#%%Fix age variables to be integer only

df_gss_older = df_gss[df_gss['age of respondent'].str.contains('older')]
df_gss.loc[df_gss_older.index,'age of respondent'] = '89'
df_gss_noage = df_gss[df_gss['age of respondent'].str.contains(':')]

df_gss_wage = df_gss.drop(df_gss_noage.index)
df_gss_wage['age of respondent'] = df_gss_wage['age of respondent'].astype('int64')

#%%add total sexual partners (both sexes)

females989 = df_gss_wage[df_gss_wage["number of female sex partner's since 18"]=="989 OR HIGHER"]
males989 = df_gss_wage[df_gss_wage["number of male sex partner's since 18"]=="989 OR HIGHER"]
df_gss_wage.loc[females989.index, "number of female sex partner's since 18"] = "989"
df_gss_wage.loc[males989.index, "number of male sex partner's since 18"] = "989"

df_gss_wage['number of sex partners since 18'] = df_gss_wage["number of female sex partner's since 18"]+df_gss_wage["number of male sex partner's since 18"]

df_gss_sex = df_gss_wage.copy()
text_answers = [':','DASH OR SLASH','REFUSED','SOME,1+','MANY,LOTS', 'SEVERAL', 'GARBLED TEXT', 'X', 'N.A']
for text in text_answers:
    df_gss_nosex = df_gss_sex[df_gss_sex['number of sex partners since 18'].str.contains(text)]
    print(text)
    print(len(df_gss_nosex))
    df_gss_sex = df_gss_sex.drop(df_gss_nosex.index)
    print(len(df_gss_sex))

df_gss_sex["number of male sex partner's since 18"] = df_gss_sex["number of male sex partner's since 18"].astype('int64')
df_gss_sex["number of female sex partner's since 18"] = df_gss_sex["number of female sex partner's since 18"].astype('int64')
df_gss_sex['number of sex partners since 18'] = df_gss_sex["number of female sex partner's since 18"]+df_gss_sex["number of male sex partner's since 18"]

#%%Filter for age

max_age = 35
min_age = 23
df_gss_agerange = df_gss_sex[df_gss_sex['age of respondent']<=max_age]
df_gss_agerange = df_gss_agerange[df_gss_agerange['age of respondent']>=min_age]

#%%Male vs female # of opposite sex partners for given percentiles

percentiles = [5,10,25,50,75,90,95]
percentiles = [x/100 for x in percentiles]

years = list(df_gss_agerange['GSS year for this respondent'].unique())

df_summary_f = pd.DataFrame(index=years,columns=percentiles)
df_summary_m = pd.DataFrame(index=years,columns=percentiles)
df_summary_f_rep = pd.DataFrame(index=years,columns=percentiles)
df_summary_m_rep = pd.DataFrame(index=years,columns=percentiles)
df_summary_f_dem = pd.DataFrame(index=years,columns=percentiles)
df_summary_m_dem = pd.DataFrame(index=years,columns=percentiles)
for year in years:
    df_year = df_gss_agerange[df_gss_agerange['GSS year for this respondent']==year]
    df_male = df_year[df_year['respondents sex']=='MALE']
    df_female = df_year[df_year['respondents sex']=='FEMALE']
    
    df_summary_f.loc[year,percentiles] = df_female.quantile(percentiles)["number of male sex partner's since 18"]
    df_summary_f.loc[year,"N"] = len(df_female)
    df_summary_f.loc[year,"% virgins"] = len(df_female[df_female["number of male sex partner's since 18"]==0])/len(df_female)
    df_summary_m.loc[year,percentiles] = df_male.quantile(percentiles)["number of female sex partner's since 18"]
    df_summary_m.loc[year,"N"] = len(df_male)
    df_summary_m.loc[year,"% virgins"] = len(df_male[df_male["number of female sex partner's since 18"]==0])/len(df_male)
    for party, df_summary_f_party, df_summary_m_party in zip(['Dem','Rep'],[df_summary_f_dem, df_summary_m_dem],[df_summary_f_rep, df_summary_m_rep]):
        df_male_party = df_male[df_male['Lumped Party']==party]
        df_female_party = df_female[df_female['Lumped Party']==party]
        
        df_summary_f_party.loc[year,percentiles] = df_female_party.quantile(percentiles)["number of male sex partner's since 18"]
        df_summary_f_party.loc[year,"N"] = len(df_female_party)
        df_summary_f_party.loc[year,"% virgins"] = len(df_female_party[df_female_party["number of male sex partner's since 18"]==0])/len(df_female_party)
        df_summary_m_party.loc[year,percentiles] = df_male_party.quantile(percentiles)["number of female sex partner's since 18"]
        df_summary_m_party.loc[year,"N"] = len(df_male_party)
        df_summary_m_party.loc[year,"% virgins"] = len(df_male_party[df_male_party["number of female sex partner's since 18"]==0])/len(df_male_party)

partners_since_18 = {}
partners_since_18['female']=df_summary_f
partners_since_18['male']=df_summary_m
partners_since_18['rep female']=df_summary_f_rep
partners_since_18['rep male']=df_summary_m_rep
partners_since_18['dem female']=df_summary_f_dem
partners_since_18['dem male']=df_summary_m_dem

#%%has there been a change in people's view of morality of extramarital sex?

df_gss_noextra = df_gss_wage[df_gss_wage['sex with person other than spouse'].str.contains(':')]
df_gss_extra = df_gss_wage.drop(df_gss_noextra.index)

#%%Filter for age

max_age = 35
min_age = 23
df_gss_agerange = df_gss_extra[df_gss_extra['age of respondent']<=max_age]
df_gss_agerange = df_gss_agerange[df_gss_agerange['age of respondent']>=min_age]

#%%Summarize opinion on extramarital sex
extra_options = list(df_gss_agerange['sex with person other than spouse'].unique())
years = list(df_gss_agerange['GSS year for this respondent'].unique())
df_extra_summary = pd.DataFrame(index=years, columns=extra_options)
df_extra_summary_m = pd.DataFrame(index=years, columns=extra_options)
df_extra_summary_f = pd.DataFrame(index=years, columns=extra_options)
df_extra_summary_rep = pd.DataFrame(index=years, columns=extra_options)
df_extra_summary_dem = pd.DataFrame(index=years, columns=extra_options)
for year in years:
    df_year = df_gss_agerange[df_gss_agerange['GSS year for this respondent']==year]
    df_year_m = df_year[df_year['respondents sex']=='MALE']
    df_year_f = df_year[df_year['respondents sex']=='FEMALE']
    df_year_rep = df_year[df_year['Lumped Party']=='Rep']
    df_year_dem = df_year[df_year['Lumped Party']=='Dem']
    for option in extra_options:
        df_year_option = df_year[df_year['sex with person other than spouse']==option]
        df_year_option_m = df_year_m[df_year_m['sex with person other than spouse']==option]
        df_year_option_f = df_year_f[df_year_f['sex with person other than spouse']==option]
        df_year_option_rep = df_year_rep[df_year_rep['sex with person other than spouse']==option]
        df_year_option_dem = df_year_dem[df_year_dem['sex with person other than spouse']==option]
        
        df_extra_summary.loc[year,option] = len(df_year_option)/len(df_year)
        df_extra_summary_m.loc[year,option] = len(df_year_option_m)/len(df_year_m)
        df_extra_summary_f.loc[year,option] = len(df_year_option_f)/len(df_year_f)
        df_extra_summary_rep.loc[year,option] = len(df_year_option_rep)/len(df_year_rep)
        df_extra_summary_dem.loc[year,option] = len(df_year_option_dem)/len(df_year_dem)

    df_extra_summary.loc[year,'N'] = len(df_year)
    df_extra_summary_m.loc[year,'N'] = len(df_year_m)
    df_extra_summary_f.loc[year,'N'] = len(df_year_f)
    df_extra_summary_rep.loc[year,'N'] = len(df_year_rep)
    df_extra_summary_dem.loc[year,'N'] = len(df_year_dem)

extra_opinion = {}
extra_opinion['all'] = df_extra_summary
extra_opinion['male'] = df_extra_summary_m
extra_opinion['female'] = df_extra_summary_f
extra_opinion['rep'] = df_extra_summary_rep
extra_opinion['dem'] = df_extra_summary_dem

#%%number of partners in past year

df_gss_nopastyr = df_gss_wage[df_gss_wage["how many sex partner's r had in last year"].str.contains(":")]
df_gss_pastyr = df_gss_wage.drop(df_gss_nopastyr.index)
df_gss_pastyr['num partners past yr'] = 0

#translate string answers to integers
pastyr_options = list(df_gss_pastyr["how many sex partner's r had in last year"].unique())

onepartner = df_gss_pastyr[df_gss_pastyr["how many sex partner's r had in last year"]==f"1 partner"]
df_gss_pastyr.loc[onepartner.index,'num partners past yr'] = 1

over100partners = df_gss_pastyr[df_gss_pastyr["how many sex partner's r had in last year"]==f"More than 100 partners"]
df_gss_pastyr.loc[over100partners.index,'num partners past yr'] = 101

oneormorepartners = df_gss_pastyr[df_gss_pastyr["how many sex partner's r had in last year"]==f"1 or more, (unspecified)"]
df_gss_pastyr.loc[oneormorepartners.index,'num partners past yr'] = 1.5

for num in range(2,5):
    numpartners = df_gss_pastyr[df_gss_pastyr["how many sex partner's r had in last year"]==f"{num} partners"]
    df_gss_pastyr.loc[numpartners.index,'num partners past yr'] = num

for low, high in zip([5,11,21],[10,20,100]):
    numpartners = df_gss_pastyr[df_gss_pastyr["how many sex partner's r had in last year"]==f"{low}-{high} partners"]
    df_gss_pastyr.loc[numpartners.index,'num partners past yr'] = (low+high)/2

#%%Filter for age

max_age = 60
min_age = 18
df_gss_agerange = df_gss_pastyr[df_gss_pastyr['age of respondent']<=max_age]
df_gss_agerange = df_gss_agerange[df_gss_agerange['age of respondent']>=min_age]

#%%Male vs female # of partners past yr for given percentiles

percentiles = [5,10,25,50,75,90,95]
percentiles = [x/100 for x in percentiles]

years = list(df_gss_agerange['GSS year for this respondent'].unique())

df_summary_f = pd.DataFrame(index=years,columns=percentiles)
df_summary_m = pd.DataFrame(index=years,columns=percentiles)
df_summary_f_rep = pd.DataFrame(index=years,columns=percentiles)
df_summary_m_rep = pd.DataFrame(index=years,columns=percentiles)
df_summary_f_dem = pd.DataFrame(index=years,columns=percentiles)
df_summary_m_dem = pd.DataFrame(index=years,columns=percentiles)
for year in years:
    df_year = df_gss_agerange[df_gss_agerange['GSS year for this respondent']==year]
    df_male = df_year[df_year['respondents sex']=='MALE']
    df_female = df_year[df_year['respondents sex']=='FEMALE']
    
    df_summary_f.loc[year,percentiles] = df_female.quantile(percentiles)['num partners past yr']
    df_summary_f.loc[year,"N"] = len(df_female)
    df_summary_f.loc[year,"% 0"] = len(df_female[df_female['num partners past yr']==0])/len(df_female)
    df_summary_m.loc[year,percentiles] = df_male.quantile(percentiles)['num partners past yr']
    df_summary_m.loc[year,"N"] = len(df_male)
    df_summary_m.loc[year,"% 0"] = len(df_male[df_male['num partners past yr']==0])/len(df_male)
    for party, df_summary_f_party, df_summary_m_party in zip(['Dem','Rep'],[df_summary_f_dem, df_summary_m_dem],[df_summary_f_rep, df_summary_m_rep]):
        df_male_party = df_male[df_male['Lumped Party']==party]
        df_female_party = df_female[df_female['Lumped Party']==party]
        
        df_summary_f_party.loc[year,percentiles] = df_female_party.quantile(percentiles)['num partners past yr']
        df_summary_f_party.loc[year,"N"] = len(df_female_party)
        df_summary_f_party.loc[year,"% 0"] = len(df_female_party[df_female_party['num partners past yr']==0])/len(df_female_party)
        df_summary_m_party.loc[year,percentiles] = df_male_party.quantile(percentiles)['num partners past yr']
        df_summary_m_party.loc[year,"N"] = len(df_male_party)
        df_summary_m_party.loc[year,"% 0"] = len(df_male_party[df_male_party['num partners past yr']==0])/len(df_male_party)

partners_past_year = {}
partners_past_year['female']=df_summary_f
partners_past_year['male']=df_summary_m
partners_past_year['rep female']=df_summary_f_rep
partners_past_year['rep male']=df_summary_m_rep
partners_past_year['dem female']=df_summary_f_dem
partners_past_year['dem male']=df_summary_m_dem

#%%save results to excel

#name output file
output = f'GSS - sexual partners since 18 - {min_age} to {max_age}.xlsx'
writer = pd.ExcelWriter(output)
for item in ['female','male','rep female','rep male','dem female','dem male']:
    partners_since_18[item].to_excel(writer,sheet_name=item)

writer.save()
writer.close()

#name output file
output = f'GSS - sexual partners past year - {min_age} to {max_age}.xlsx'
writer = pd.ExcelWriter(output)
for item in ['female','male','rep female','rep male','dem female','dem male']:
    partners_past_year[item].to_excel(writer,sheet_name=item)

writer.save()
writer.close()

#name output file
output = f'GSS - opinion of extramarital sex - {min_age} to {max_age}.xlsx'
writer = pd.ExcelWriter(output)
for item in ['all','female','male','rep','dem']:
    extra_opinion[item].to_excel(writer,sheet_name=item)
    
writer.save()
writer.close()