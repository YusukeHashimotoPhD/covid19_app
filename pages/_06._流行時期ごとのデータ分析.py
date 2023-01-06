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

st.title("流行時期ごとのデータ分析")
st.write('新型コロナウィルスは定期的に変異を繰り返しながら、流行と収束を繰り返しています。その周期は4ヶ月ほどで、各々の流行における重なりが少ないことが特徴です。このため特定期間のデータを抽出することで、それぞれの変異株の特徴を分析できると考えられます。このページは流行時期によって抽出されたデータの分析を行います。')
#st.write('特に、ワクチンの普及によるオミクロン株への変異による感染力の飛躍的増加が、時系列データに与えた影響が顕著です。')


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

dict_start_day = {
    '第1波': '2020-01-01',
    '第2波': '2020-07-10',
    '第3波': '2020-10-01',
    '第4波': '2021-03-25',
    '第5波': '2021-07-15',
    '第6波': '2021-12-10',
    '第7波': '2022-06-15',
    '第8波': '2022-10-14',
    '全データ': '2020-01-01',
    '第1波~第5波': '2020-01-01',
    '第6波以降': '2021-12-10',
    }

dict_finish_day = {
    '第1波': '2020-07-10',
    '第2波': '2020-10-01',
    '第3波': '2021-03-25',
    '第4波': '2021-07-15',
    '第5波': '2021-12-10',
    '第6波': '2022-06-15',
    '第7波': '2022-10-14',
    '第8波': df.index[-1].strftime('%Y-%m-%d'),
    '全データ': df.index[-1].strftime('%Y-%m-%d'),
    '第1波~第5波': '2021-12-10',
    '第6波以降': df.index[-1].strftime('%Y-%m-%d'),
    }

text_waves = '''
第1波: 2020年1月1日~\n
第2波: 2020年7月10日~\n
第3波: 2020年10月1日~\n
第4波: 2021年3月25日~\n
第5波: 2021年7月15日~\n
第6波: 2021年12月10日~\n
第7波: 2022年6月15日~\n
第8波: 2022年10月14日~\n
'''

with st.sidebar:
    selected_wave = st.selectbox(
        '流行時期の選択',
        dict_start_day.keys(),
        index=len(dict_start_day)-3
    )

    st.write(text_waves)

start_day = datetime.datetime.strptime(dict_start_day[selected_wave], '%Y-%m-%d')
finish_day = datetime.datetime.strptime(dict_finish_day[selected_wave], '%Y-%m-%d')

if moving_average == 'なし':
    df_a = df
else:
    df_a = df.rolling(7).mean()

df_a = df_a[df_a.index >= start_day]
df_a = df_a[df_a.index <= finish_day]

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

#st.subheader('都道府県別 ' + data_kind + 'の時系列データ2次元プロット')
# 2次元データ
fig = px.imshow(df_a.T,
                height=800,
                width=800,
                )
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
    #    title=data_kind,
    xaxis_title="日時",
    yaxis_title="都道府県名",
)
st.plotly_chart(fig)
#st.plotly_chart(fig, use_container_width=True)

st.subheader('都道府県別 ' + data_kind + '時系列データの相関係数')

# 相関係数
corr = df_a.corr()
fig = px.imshow(corr,
                height=800,
                width=800,
                )
st.plotly_chart(fig)
#st.plotly_chart(fig, use_container_width=True)

st.subheader('都道府県別 ' + data_kind + '時系列データの主成分分析')

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
#    title='都道府県別時系列データの主成分分析',
    xaxis_title="第1主成分",
    yaxis_title="第2主成分",
)
fig.update_traces(textposition='top center')
#st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig)
