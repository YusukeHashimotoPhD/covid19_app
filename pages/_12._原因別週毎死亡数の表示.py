import pandas as pd
import plotly.express as px
import streamlit as st


# file_path = '/Users/yusukehashimoto/Downloads/Observed/Observed_Cancer.csv'
# df = pd.read_csv(file_path)
#
# df['date'] = pd.to_datetime(df['week_ending_date'], format='%d%b%Y')
# dfA=df[df['prefectureJP'] == '全国']
#

def calc_days_from_new_year(date):
    ny = date.replace(month=1, day=1)
    return (date - ny).days


def calc_weeks_from_new_year(date):
    ny = date.replace(month=1, day=1)
    return int((date - ny).days / 7)


def plot_data(df, data_name, label_y):
    dfp = df.pivot(index='weeks_from_ny', columns='year', values=data_name)
    dfp = dfp.drop(2010, axis=1)
    # dfp = dfp.T
    # dfp = dfp - dfp.mean()
    # dfp = dfp.T
    fig = px.line(
        dfp,
        title=label_y,
    )
    fig.update_layout(
        xaxis_title="年初からの週数",
        yaxis_title=label_y,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_normalized_data(df, data_name, label_y):
    dfp = df.pivot(index='weeks_from_ny', columns='year', values=data_name)
    dfp = dfp.drop(2010, axis=1)
    dfp = dfp.T
    dfp = dfp - dfp.mean()
    dfp = dfp.T
    fig = px.line(
        dfp,
        title=label_y,
    )
    fig.update_layout(
        xaxis_title="年初からの週数",
        yaxis_title=label_y,
    )
    st.plotly_chart(fig, use_container_width=True)


st.title('原因別週毎死亡数')

st.write('Data source: https://exdeaths-japan.org/#interpretation')

folder_path = './data/Observed/'
list_data = ['Observed_Cancer', 'Observed_Circulatory', 'Observed_non-COVID-19', 'Observed_Respiratory',
             'Observed_Senility', 'Observed_Suicide']

df_s = pd.DataFrame()
for file_name in list_data:
    file_path = folder_path + file_name + '.csv'
    df = pd.read_csv(file_path)
    dfA = df[df['prefectureJP'] == '全国']
    df_s[file_name] = dfA['Observed']

dfA = df[df['prefectureJP'] == '全国']
dfA['date'] = pd.to_datetime(dfA['week_ending_date'], format='%d%b%Y')
dfB = dfA[['date']]
dfB['date'] = pd.to_datetime(dfB['date'])
dfC = pd.concat([dfB, df_s], axis=1)
dfC.index = dfC['date']
dfC = dfC.drop('date', axis=1)

file_path = './data/Observed-2.csv'
file_path = 'https://exdeaths-japan.org/data/Observed.csv'
dfF = pd.read_csv(file_path)
dfF['date'] = pd.to_datetime(dfF['week_ending_date'], format='%d%b%Y')
dfA = dfF[dfF['prefectureJP'] == '全国']
dfB = dfA[['date', 'Observed']]
dfB['date'] = pd.to_datetime(dfB['date'])
dfB['year'] = dfB['date'].dt.year
#dfB['days_from_ny'] = dfB['date'].map(lambda x: calc_days_from_new_year(x))
dfB['weeks_from_ny'] = dfB['date'].map(lambda x: calc_weeks_from_new_year(x))
dfB.index = dfB['date']
dfB = dfB.rename(columns={'Observed': 'Observed_all'})
dfG = pd.concat([dfB, dfC], axis=1)
dfH = dfG.dropna()

# list_data = ['Observed_Cancer', 'Observed_Circulatory', 'Observed_non-COVID-19', 'Observed_Respiratory',
#              'Observed_Senility', 'Observed_Suicide']

plot_data(dfH, 'Observed_all', '週毎の死亡数')
plot_data(dfH, 'Observed_non-COVID-19', 'covid-19以外による週毎の死亡数')
plot_data(dfH, 'Observed_Circulatory', '循環器系による週毎の死亡数')
plot_data(dfH, 'Observed_Respiratory', '呼吸器疾患による週毎の死亡数')
plot_data(dfH, 'Observed_Cancer', 'がんによる週毎の死亡数')
plot_data(dfH, 'Observed_Senility', '老衰による週毎の死亡数')
plot_data(dfH, 'Observed_Suicide', '自殺による週毎の死亡数')


st.title('原因別週毎死亡数の年別変化量')
st.write('統計学的に正しいのかは微妙ですが、それぞれの週毎の年平均を引き、年毎の変化量を求めました。')

plot_normalized_data(dfH, 'Observed_all', '週毎の死亡数変化量')
plot_normalized_data(dfH, 'Observed_non-COVID-19', 'covid-19以外による週毎の死亡数変化量')
plot_normalized_data(dfH, 'Observed_Circulatory', '循環器系による週毎の死亡数変化量')
plot_normalized_data(dfH, 'Observed_Respiratory', '呼吸器疾患による週毎の死亡数変化量')
plot_normalized_data(dfH, 'Observed_Cancer', 'がんによる週毎の死亡数変化量')
plot_normalized_data(dfH, 'Observed_Senility', '老衰による週毎の死亡数変化量')
plot_normalized_data(dfH, 'Observed_Suicide', '自殺による週毎の死亡数変化量')
