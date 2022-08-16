import pandas as pd
import streamlit as st
import plotly.express as px

#from datetime import datetime
import datetime

st.set_page_config(layout="wide")

st.title("クラスタの発生状況")
st.caption('厚生労働省が発表したデータをグラフ化しています。　https://covid19.mhlw.go.jp/extensions/public/index.html')

#file_path = '/Users/yusukehashimoto/Downloads/cluster_events_weekly.csv'
url = 'https://covid19.mhlw.go.jp/public/opendata/cluster_events_weekly.csv'

df = pd.read_csv(url, index_col = 0)
columns = ['県', '合計', '医療機関', '福祉施設', '高齢者福祉施設', '児童福祉施設', '障害者福祉施設', '飲食店', '運動施設等', '学校・教育施設等', '企業等', 'その他']
df.columns = columns

fig = px.line(df.iloc[:,2:])
fig.update_layout(
    title='クラスタ発生場所の時系列変化',
    xaxis_title="場所",
    yaxis_title="クラスタ発生数",
)
st.plotly_chart(fig, use_container_width=True)

df_a = df.drop('福祉施設', axis = 1)
fig = px.bar(df_a.iloc[:,2:])
fig.update_layout(
    title='クラスタ発生場所の時系列変化',
    xaxis_title="週",
    yaxis_title="クラスタ発生数",
)
st.plotly_chart(fig, use_container_width=True)

fig = px.imshow(df.iloc[:,2:], aspect="auto", height=800)
fig.update_layout(
    title='クラスタ発生場所',
    xaxis_title="場所",
    yaxis_title="週",
)
st.plotly_chart(fig, use_container_width=True)