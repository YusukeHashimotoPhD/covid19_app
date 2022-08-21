import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout="wide")

st.title("クラスタの発生状況の表示")
st.write('人から人へ感染する新型コロナウィルスは、集団感染を起こします。これをクラスタといい、感染拡大を抑えるために集中的な対処が望まれます。ここでは、厚生労働省が公開するクラスタの発生状況を表示します。')


@st.cache
def load_data():
    url = 'https://covid19.mhlw.go.jp/public/opendata/cluster_events_weekly.csv'
    df = pd.read_csv(url, index_col=0)
    columns = ['県', '合計', '医療機関', '福祉施設', '高齢者福祉施設', '児童福祉施設', '障害者福祉施設', '飲食店', '運動施設等', '学校・教育施設等', '企業等', 'その他']
    df.columns = columns
    return df


df = load_data()

st.subheader('クラスタ発生場所の時系列変化')

fig = px.line(df.iloc[:, 2:])
fig.update_layout(
#    title='クラスタ発生場所の時系列変化',
    xaxis_title="週",
    yaxis_title="クラスタの発生数",
)
st.plotly_chart(fig, use_container_width=True)

df_a = df.drop('福祉施設', axis=1)
fig = px.bar(df_a.iloc[:, 2:])
fig.update_layout(
#    title='クラスタ発生場所の時系列変化',
    xaxis_title="週",
    yaxis_title="クラスタの発生数",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('クラスタ発生場所時系列変化の2次元プロット')

fig = px.imshow(df.iloc[:, 2:].T, aspect="auto")
fig.update_layout(
#    title='クラスタ発生場所',
    yaxis_title="クラスタの発生場所",
    xaxis_title="週",
)
st.plotly_chart(fig, use_container_width=True)
