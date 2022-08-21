import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.decomposition import PCA

import datetime


#@st.cache(allow_input_mutation=True)
@st.cache(allow_output_mutation=True)
def data_load(url):
    df_t = pd.read_csv(url, index_col=0)
    df = df_t.iloc[:, 1:]
    list_prefacture = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都',
                       '神奈川県',
                       '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
                       '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
                       '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
    df.columns = list_prefacture
    df.index = pd.to_datetime(df.index)
    return df


st.set_page_config(layout="wide")

st.title("都道府県別日毎データの表示")

dict_data = {
    '新規感染者数': 'newly_confirmed_cases_daily',
    '10万人あたりの新規感染者数': 'newly_confirmed_cases_per_100_thousand_population_daily',
    #    '治療必要者数': 'requiring_inpatient_care_etc_daily',
    '重症患者数': 'severe_cases_daily',
    '死亡者数': 'deaths_cumulative_daily',
}

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['新規感染者数'] + '.csv'
df_new = data_load(url)

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['10万人あたりの新規感染者数'] + '.csv'
df_new_10 = data_load(url)

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['重症患者数'] + '.csv'
df_severe = data_load(url)

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['死亡者数'] + '.csv'
df_deathA = data_load(url)
df_death = df_deathA.diff()

st.write('表示するデータの日付を選択してください。')

selected_day = st.slider(
    '',
    min_value=df_new.index[0].to_pydatetime(),
    max_value=df_new.index[-1].to_pydatetime(),
    value=df_new.index[-1].to_pydatetime(),
    format="YY年MM月DD日",
)

selected_datetime = datetime.datetime(selected_day.year, selected_day.month, selected_day.day)

def make_graph(df, selected_datetime, label):
    data = df[df.index == selected_datetime]
    fig = px.bar(data.T, orientation='h', height = 800)
    fig.update_layout(
        title= label,
        xaxis_title= label,
        yaxis_title="都道府県",
        showlegend=False,
    )
    return fig

col0, col1, col2, col3 = st.columns(4)

with col0:
    fig = make_graph(df_new_10, selected_datetime, '10万人あたりの新規感染者数')
    st.plotly_chart(fig, use_container_width=True)

with col1:
    fig = make_graph(df_new, selected_datetime, '新規感染者数')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = make_graph(df_severe, selected_datetime, '重症患者数')
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = make_graph(df_death, selected_datetime, '死亡者数')
    st.plotly_chart(fig, use_container_width=True)

st.write('データ')
url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['新規感染者数'] + '.csv'
st.caption(url)

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['10万人あたりの新規感染者数'] + '.csv'
st.caption(url)

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['重症患者数'] + '.csv'
st.caption(url)

url = 'https://covid19.mhlw.go.jp/public/opendata/' + dict_data['死亡者数'] + '.csv'
st.caption(url)
