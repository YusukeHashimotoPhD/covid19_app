import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.decomposition import PCA

#from datetime import datetime
import datetime

st.set_page_config(layout="wide")

st.title("全国のデータ分析")
st.caption('厚生労働省が発表したデータをグラフ化しています。　https://covid19.mhlw.go.jp/extensions/public/index.html')

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

st.write('データ: ' + url)

if data_kind == '死亡者数':
    df = df.diff()

df.columns = list_prefacture
df.index = pd.to_datetime(df.index)

# selected_day = st.slider(
#     "日時の選択",
#     min_value=df.index[0].to_pydatetime(),
#     max_value=df.index[-1].to_pydatetime(),
#     value=df.index[-1].to_pydatetime(),
#     format="YY年MM月DD日",
# )

selected_day_1 = st.date_input(
    "日時の選択",
    min_value=df.index[0].to_pydatetime(),
    max_value=df.index[-1].to_pydatetime(),
    value=df.index[-1].to_pydatetime(),
)

selected_datetime = datetime.datetime(selected_day_1.year, selected_day_1.month, selected_day_1.day)

#st.write(selected_day, selected_day_1, selected_datetime)

data = df[df.index == selected_datetime]
fig = px.bar(data.T)
fig.update_layout(
    title='都道府県別 ' + data_kind,
    yaxis_title=data_kind,
    xaxis_title="都道府県",
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('下のスライダーで、分析する時系列データの範囲を選択できます。')

start_time, finish_time = st.slider(
    "",
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

# 時系列データ
list_data = df.columns
fig = px.line(df_a, y=list_data)
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
    title='都道府県別 ' + data_kind + 'の時系列データ',
    yaxis_title=data_kind,
    xaxis_title="日時",
)

st.plotly_chart(fig, use_container_width=True)

# 2次元データ
fig = px.imshow(df_a.T, height=800)
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
#    title=data_kind,
    xaxis_title="日時",
    yaxis_title="都道府県名",
)
st.plotly_chart(fig, use_container_width=True)

# 相関係数
corr = df_a.corr()
fig = px.imshow(corr, height=800)
fig.update_layout(
    title='都道府県別時系列データの相関係数',
#    xaxis_title="第1主成分",
#    yaxis_title="第2主成分",
)
st.plotly_chart(fig, use_container_width=True)

# 主成分分析
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
fig.update_layout(
    title='都道府県別時系列データの主成分分析',
    xaxis_title="第1主成分",
    yaxis_title="第2主成分",
)
st.plotly_chart(fig, use_container_width=True)
