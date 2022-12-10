import pandas as pd
import plotly.express as px


folder_path = './Observed/'
list_data = ['Observed_Cancer', 'Observed_Circulatory', 'Observed_non-COVID-19', 'Observed_Respiratory', 'Observed_Senility', 'Observed_Suicide']

df_s = pd.DataFrame()

for file_name in list_data:
    file_path = folder_path + file_name + '.csv'
    df = pd.read_csv(file_path)
    dfA=df[df['prefectureJP'] == '全国']
    df_s[file_name] = dfA['Observed']

dfA['date'] = pd.to_datetime(dfA['week_ending_date'], format='%d%b%Y')
dfB=dfA[['date']]
dfB['date'] = pd.to_datetime(dfB['date'])
dfC = pd.concat([dfB, df_s], axis=1)
dfC.index=dfC['date']
dfC = dfC.drop('date', axis=1)

file_path = './Observed-2.csv'
dfF= pd.read_csv(file_path)
dfF['date'] = pd.to_datetime(dfF['week_ending_date'], format='%d%b%Y')
dfA=dfF[dfF['prefectureJP'] == '全国']
dfB=dfA[['date', 'Observed']]
dfB['date'] = pd.to_datetime(dfB['date'])
dfB.index=dfB['date']
dfB = dfB.drop('date', axis=1)
dfB = dfB.rename(columns={'Observed':'Observed_all'})
dfG = pd.concat([dfB, dfC], axis=1)

fig = px.scatter(
    dfG
)
fig.show()