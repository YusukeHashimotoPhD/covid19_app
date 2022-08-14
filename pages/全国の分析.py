import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.decomposition import PCA

from datetime import datetime

st.set_page_config(layout="wide")

st.title("covid-19のデータ分析")
st.caption('厚生労働省が発表したデータをグラフ化しています。（https://covid19.mhlw.go.jp/extensions/public/index.html）')

dict_data = {
    '新規感染者数': 'newly_confirmed_cases_daily',
    '10万人あたりの新規感染者数': 'newly_confirmed_cases_per_100_thousand_population_daily',
    #    '治療必要者数': 'requiring_inpatient_care_etc_daily',
    '重症患者数': 'severe_cases_daily',
    '死亡者数': 'deaths_cumulative_daily',
}

list_prefacture = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
                   '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
                   '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
                   '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

with st.sidebar:

    data_kind = st.selectbox(
        'データの種類',
        list(dict_data.keys()),
        index=0
    )

    moving_average = st.selectbox(
        '移動平均',
        ['なし', 'あり（7日）'],
        index=1
    )

url_1 = 'https://covid19.mhlw.go.jp/public/opendata/'
url = url_1 + dict_data[data_kind] + '.csv'
df_t = pd.read_csv(url, index_col=0)
df = df_t.iloc[:, 1:]

if data_kind == '死亡者数':
    df = df.diff()

df.columns = list_prefacture
df.index = pd.to_datetime(df.index)

selected_day = st.slider(
    "表示",
    min_value=df.index[0].to_pydatetime(),
    max_value=df.index[-1].to_pydatetime(),
    value=df.index[-1].to_pydatetime(),
    format="YY年MM月DD日",
)

data = df[df.index == selected_day]
fig = px.bar(data.T)
st.plotly_chart(fig, use_container_width=True)

start_time, finish_time = st.slider(
    "分析範囲",
    min_value=df.index[0].to_pydatetime(),
    max_value=df.index[-1].to_pydatetime(),
    #    value=datetime(2020, 1, 1, 9, 30),
    format="YY年MM月DD日",
    value=[df.index[0].to_pydatetime(), df.index[-1].to_pydatetime()]
)

if moving_average == 'なし':
    df_a = df
else:
    df_a = df.rolling(7).mean()

df_a = df_a[df_a.index >= start_time]
df_a = df_a[df_a.index <= finish_time]

list_data = df.columns
fig = px.line(df_a, y=list_data)
st.plotly_chart(fig, use_container_width=True)

fig = px.imshow(df_a.T, height=800)
st.plotly_chart(fig, use_container_width=True)

corr = df_a.corr()
fig = px.imshow(corr, height=800)
st.plotly_chart(fig, use_container_width=True)
# if __name__ == '__main__':
#    print('PyCharm')

df_b = df_a.dropna(axis = 0)
PCAa = PCA(n_components=2)
X_pca = PCAa.fit_transform(df_b.T)
fig = px.scatter(
    x=X_pca[:, 0],
    y=X_pca[:, 1],
    text=list_prefacture,
    height = 800,
    width=800,
)
st.plotly_chart(fig, use_container_width=True)
