import pandas as pd
import plotly.express as px

st.write('Data source: https://exdeaths-japan.org/#interpretation')


def calc_days_from_new_year(date):
    ny = date.replace(month=1, day=1)
    return (date - ny).days


def calc_weeks_from_new_year(date):
    ny = date.replace(month=1, day=1)
    return (date - ny).days / 7


folder_path = './data/Observed/'
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

file_path = 'data/Observed-2.csv'
dfF= pd.read_csv(file_path)
dfF['date'] = pd.to_datetime(dfF['week_ending_date'], format='%d%b%Y')
dfA=dfF[dfF['prefectureJP'] == '全国']
dfB=dfA[['date', 'Observed']]
dfB['date'] = pd.to_datetime(dfB['date'])
dfB['year'] = dfB['date'].dt.year
dfB['days_from_ny'] = dfB['date'].map(lambda x: calc_days_from_new_year(x))
dfB['weeks_from_ny'] = dfB['date'].map(lambda x: calc_weeks_from_new_year(x))
dfB.index=dfB['date']
dfB = dfB.rename(columns={'Observed':'Observed_all'})
dfB = dfB.dropna()
dfG = pd.concat([dfB, dfC], axis=1)

fig = px.scatter(
    dfG,
    x='weeks_from_ny',
    y=['Observed_all'] + list_data,
    symbol='year',
    hover_name='date',
)
fig.show()