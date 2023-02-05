import requests
import zipfile
import pandas as pd
import datetime
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def load_data():
    file_path = 'https://exdeaths-japan.org/data/Observed.csv'
    return pd.read_csv(file_path)


def calc_days_from_new_year(date):
    ny = date.replace(month=1, day=1)
    return (date - ny).days


def calc_weeks_from_new_year(date):
    ny = date.replace(month=1, day=1)
    return (date - ny).days / 7


st.title('都道府県別週毎死亡数')

df = load_data()

df['date'] = pd.to_datetime(df['week_ending_date'], format='%d%b%Y')
df = df.sort_values('date')
df.index = df['date']
df = df.drop(['week_ending_date', 'date'], axis=1)

dt1 = datetime.datetime(year=2012, month=1, day=1, hour=0)
df['daysA'] = df.index - dt1
df['days'] = df['daysA'].dt.days

list_index = df.index
for index in list_index:
    df.loc[index, 'new_year'] = index.replace(month=1, day=1)
    df.loc[index, 'days_from_NY'] = index - df.loc[index, 'new_year']

df['days_from_NY'] = df.index - df['new_year']
df['days_from_NY'] = df['days_from_NY'].dt.days
df['year'] = df.index.year

dfA = df[df['days'] > 0]
dfA = dfA[dfA['prefectureJP'] != '全国']
dfA['year'] = dfA['year'].astype(str)

dfB = dfA.pivot(columns='prefectureJP', values='Observed')
dfC = dfB / dfB.mean()
dfC['date'] = dfC.index
dfD = pd.melt(dfC, id_vars='date', var_name='prefectureJP', value_name='Observed')

dfD['days_from_ny'] = dfD['date'].map(lambda x: calc_days_from_new_year(x))
dfD['weeks_from_ny'] = dfD['date'].map(lambda x: calc_weeks_from_new_year(x))
dfD['year'] = dfD['date'].dt.year
dfD['year'] = dfD['year'].astype(str)

st.dataframe(dfA)

fig = px.scatter(dfA,
                 x='weeks_from_ny',
                 y='Observed',
                 color='prefectureJP'
                 )

fig.update_layout(
    xaxis_title="年始からの週数",
    yaxis_title="死亡数",
)
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(dfD,
                 x='weeks_from_ny',
                 y='Observed',
                 color='prefectureJP',
                 hover_name='prefectureJP',
                 hover_data=['date']
                 )
fig.update_layout(
    xaxis_title="年始からの週数",
    yaxis_title="死亡数の相対的変化",
)
st.plotly_chart(fig, use_container_width=True)
