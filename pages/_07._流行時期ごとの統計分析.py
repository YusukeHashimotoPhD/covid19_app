import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.title("流行時期ごとの統計分析")
st.write('新型コロナウィルスは定期的に変異を繰り返しながら、流行と収束を繰り返しています。その周期は4'
         'ヶ月ほどで、各々の流行における重なりが少ないことが特徴です。このため特定期間のデータを抽出することで、それぞれの変異株の特徴を分析できると考えられます。このページは流行時期によって抽出されたデータの統計分析を行います。初期設定は日本全国です。左のサイドバーに記した期間を流行時と定義します。また、左のサイドバーから分析するデータの都道府県を選択できます。')


#@st.cache
def load_data(data_name, list_prefacture):
    dict_data = {
        '新規感染者数': 'newly_confirmed_cases_daily',
        #'10万人あたりの新規感染者数': 'newly_confirmed_cases_per_100_thousand_population_daily',
        #    '治療必要者数': 'requiring_inpatient_care_etc_daily',
        '重症患者数': 'severe_cases_daily',
        '死亡者数': 'deaths_cumulative_daily',
    }

    url = f'https://covid19.mhlw.go.jp/public/opendata/{dict_data[data_name]}.csv'
    df = pd.read_csv(url, index_col=0)

    df.columns = list_prefacture
    df.index = pd.to_datetime(df.index)

    dict_start_time = {
        '第1波': '2020-01-01',
        '第2波': '2020-07-10',
        '第3波': '2020-10-01',
        '第4波': '2021-03-25',
        '第5波': '2021-07-15',
        '第6波': '2021-12-10',
        '第7波': '2022-06-15',
        '第8波': '2022-10-14',
    }

    dict_finish_time = {
        '第1波': '2020-07-10',
        '第2波': '2020-10-01',
        '第3波': '2021-03-25',
        '第4波': '2021-07-15',
        '第5波': '2021-12-10',
        '第6波': '2022-06-15',
        '第7波': '2022-10-14',
        '第8波': df.index[-1].to_pydatetime(),
    }

    if data_name == '死亡者数':
        df = df.diff()

    for 流行時期 in dict_finish_time.keys():
        mask = (df.index >= dict_start_time[流行時期]) & (df.index < dict_finish_time[流行時期])
        df.loc[mask, '流行時期'] = 流行時期

    return df


def make_bargraph(df, data_name, prefecture):
    fig = px.bar(df, x='流行時期', y=prefecture, color='流行時期')
    fig.update_layout(
        title=data_name,
        xaxis_title="流行時期",
        yaxis_title=data_name,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

def make_boxgraph(df, data_name, prefecture):
    fig = px.box(df, x='流行時期', y=prefecture, color='流行時期', points="all")
    fig.update_layout(
        title=data_name,
        xaxis_title="流行時期",
        yaxis_title=data_name,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

def make_linegraph(df, data_name, prefecture):
    fig = px.line(df, y=prefecture, color='流行時期')
    fig.update_layout(
        title=data_name,
        xaxis_title="日付",
        yaxis_title=data_name,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

list_prefacture = ['全国', '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都',
                   '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府',
                   '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
                   '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

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

list_data_name = ['新規感染者数', '重症患者数', '死亡者数']
with st.sidebar:
    prefecture = st.selectbox(
        '都道府県',
        list_prefacture,
        0
    )

    st.write(text_waves)

for data_name in list_data_name:
    df = load_data(data_name, list_prefacture)
    fig = px.line(df, y=prefecture, color='流行時期')
    fig.update_xaxes(tickformat="%Y年%m月")
    fig.update_layout(
        xaxis_title="日付",
        yaxis_title=data_name,
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader('流行期ごとの時系列データ')
st.write('新規感染者、重症患者数、死亡者数の流行期ごとの時系列データを表示します。')

col0, col1, col2 = st.columns(3)

with col0:
    data_name = '新規感染者数'
    df = load_data(data_name, list_prefacture)
    make_linegraph(df, data_name, prefecture)

with col1:
    data_name = '重症患者数'
    df = load_data(data_name, list_prefacture)
    make_linegraph(df, data_name, prefecture)

with col2:
    data_name = '死亡者数'
    df = load_data(data_name, list_prefacture)
    make_linegraph(df, data_name, prefecture)

st.subheader('流行期ごとの統計分析')
st.write('最初にbar plotを、次にbox plotを示します。')

col0, col1, col2 = st.columns(3)

with col0:
    data_name = '新規感染者数'
    df = load_data(data_name, list_prefacture)
    make_bargraph(df, data_name, prefecture)

with col1:
    data_name = '重症患者数'
    df = load_data(data_name, list_prefacture)
    make_bargraph(df, data_name, prefecture)

with col2:
    data_name = '死亡者数'
    df = load_data(data_name, list_prefacture)
    make_bargraph(df, data_name, prefecture)

#st.caption('バープロットは、それぞれの流行期での総計値を示します。オミクロン株に変異した第6波以降、死者数が急増していることが見てとれます。')
#st.write('次に、ボックスプロットを示します。')

col0, col1, col2 = st.columns(3)

with col0:
    data_name = '新規感染者数'
    df = load_data(data_name, list_prefacture)
    make_boxgraph(df, data_name, prefecture)

with col1:
    data_name = '重症患者数'
    df = load_data(data_name, list_prefacture)
    make_boxgraph(df, data_name, prefecture)

with col2:
    data_name = '死亡者数'
    df = load_data(data_name, list_prefacture)
    make_boxgraph(df, data_name, prefecture)

#st.caption('ボックスプットは、日毎の感染状況を示します。オミクロン株に変異した第6波以降、新規感染者数が急増し、重症者数は抑えられていますが、死者数は増えていることが見てとれます。')
