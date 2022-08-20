import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.decomposition import PCA

import datetime


@st.cache(allow_output_mutation=True)
def data_load(url):
    df_t = pd.read_csv(url, index_col=0)
    df = df_t.iloc[:, 1:]
    return df


st.set_page_config(layout="wide")

st.title("都道府県別データの分析")
st.write('新型コロナウィルスは人から人への感染を繰り返しながら広がっていきます。このため、人の流れが感染状況に反映されるものと考えられます。このページは、感染状況の都道府県ごとの関係を分析するデータを提供します。どうぞご活用ください。')
#https://covid19.mhlw.go.jp/extensions/public/index.html'

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
        index=1
    )

    moving_average = st.selectbox(
        '移動平均',
        ['なし', 'あり（7日）'],
        index=1
    )

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data[data_kind] + '.csv'
st.write('データ: ' + url)
df = data_load(url)

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

# selected_day_1 = st.date_input(
#     "日時の選択",
#     min_value=df.index[0].to_pydatetime(),
#     max_value=df.index[-1].to_pydatetime(),
#     value=df.index[-1].to_pydatetime(),
# )

# selected_datetime = datetime.datetime(selected_day_1.year, selected_day_1.month, selected_day_1.day)

# st.write(selected_day, selected_day_1, selected_datetime)

# st.subheader('下のスライダーで、分析する時系列データの範囲を選択できます。')
#
# start_time, finish_time = st.slider(
#     "",
#     min_value=df.index[0].to_pydatetime(),
#     max_value=df.index[-1].to_pydatetime(),
#     #    value=datetime(2020, 1, 1, 9, 30),
#     format="YY年MM月DD日",
#     value=[df.index[0].to_pydatetime(), df.index[-1].to_pydatetime()]
# )

if moving_average == 'なし':
    df_a = df
else:
    df_a = df.rolling(7).mean()

# df_a = df_a[df_a.index >= start_time]
# df_a = df_a[df_a.index <= finish_time]

st.subheader('都道府県別 ' + data_kind + 'の時系列データ')
st.write('最初に、都道府県別データの時系列データをプロットします。データの種類は、左タブから選択できます。また、データは曜日によって大きく変動します。この変動は一週間の移動平均をとることで抑えることができ、これも左タブの「移動平均」から選択できます。')

# 時系列データ
list_data = df.columns
fig = px.line(df_a, y=list_data)
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
#    title='都道府県別 ' + data_kind + 'の時系列データ',
    yaxis_title=data_kind,
    xaxis_title="日時",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('都道府県別 ' + data_kind + 'の時系列データ2次元プロット')

# 2次元データ
fig = px.imshow(df_a.T, height=800)
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
    #    title=data_kind,
    xaxis_title="日時",
    yaxis_title="都道府県名",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('都道府県別 ' + data_kind + 'の時系列データ相関係数')

st.write('次に、都道府県別時系列データの相関係数を示します。例えば新規感染者数の相関係数は予想通り、地理的に近い都道府県の相関が強い傾向を顕著に示します。例えば、関東の東京都、神奈川県、千葉県、埼玉県、また、関西の大阪府、京都府、滋賀県、兵庫県、奈良県の相関係数が非常に高くなっています。さらに、これら関東と関西の都市圏の相関係数も高くなっていることが興味深いです。最後に、島根県と全ての都道府県の相関係数が低いことが不思議です。')
# 相関係数
corr = df_a.corr()
fig = px.imshow(corr, height=800)
# fig.update_layout(
# #    title='都道府県別時系列データの相関係数',
#     #    xaxis_title="第1主成分",
#     #    yaxis_title="第2主成分",
# )
st.plotly_chart(fig, use_container_width=True)

st.subheader('都道府県別 ' + data_kind + 'の時系列データ主成分分析')

st.write('最後に、都道府県別時系列データの主成分分析を示します。例えば、新規感染者数の相関係数は東京都と大阪府が近しい関係にあること、そして沖縄県がこれらと異なる傾向を示すことが見て取れます。ただし、新型コロナウィルスは変異を繰り返しながら流行と収束を繰り返しており、その感染状況も変異種により大きく異なります。このことを分析するには、それぞれの変異種が流行した期間ごとのデータを分析する必要があります。左タブの「」のページで分析できますので、どうぞご活用ください。')
# 主成分分析
df_b = df_a.dropna(axis=0)
PCAa = PCA(n_components=2)
X_pca = PCAa.fit_transform(df_b.T)
fig = px.scatter(
    x=X_pca[:, 0],
    y=X_pca[:, 1],
    text=list_prefacture,
    height=800,
    width=800,
)
fig.update_layout(
    title='都道府県別時系列データの主成分分析',
    xaxis_title="第1主成分",
    yaxis_title="第2主成分",
)
st.plotly_chart(fig, use_container_width=True)

# data = df[df.index == selected_datetime]
#
# fig = px.bar(data.T, orientation='h', height = 800)
# fig.update_layout(
#     title='都道府県別 ' + data_kind,
#     xaxis_title=data_kind,
#     yaxis_title="都道府県",
#     showlegend=False,
# )
# st.plotly_chart(fig, use_container_width=True)
