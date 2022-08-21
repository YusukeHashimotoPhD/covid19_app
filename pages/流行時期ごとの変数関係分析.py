import pandas as pd
import plotly.express as px
import streamlit as st


def load_data(prefacture, list_data_kind):
    url_1 = 'https://covid19.mhlw.go.jp/public/opendata/'

    data_kind = list_data_kind[0]
    url = url_1 + dict_data[data_kind] + '.csv'
    df_0 = pd.read_csv(url, index_col=0)
    df_0.columns = list_prefacture

    data_kind = list_data_kind[1]
    url = url_1 + dict_data[data_kind] + '.csv'
    df_1 = pd.read_csv(url, index_col=0)
    df_1.columns = list_prefacture

    data_kind = list_data_kind[2]
    url = url_1 + dict_data[data_kind] + '.csv'
    df_2 = pd.read_csv(url, index_col=0)
    df_2.columns = list_prefacture

    data_kind = list_data_kind[3]
    url = url_1 + dict_data[data_kind] + '.csv'
    df_3A = pd.read_csv(url, index_col=0)
    df_3 = df_3A.diff()
    df_3.columns = list_prefacture

    data_kind = list_data_kind[4]
    url = url_1 + dict_data[data_kind] + '.csv'
    df_4A = pd.read_csv(url, index_col=0)
    df_4 = df_4A[
        ['(ALL) Requiring inpatient care', '(Hokkaido) Requiring inpatient care', '(Aomori) Requiring inpatient care',
         '(Iwate) Requiring inpatient care', '(Miyagi) Requiring inpatient care', '(Akita) Requiring inpatient care',
         '(Yamagata) Requiring inpatient care', '(Fukushima) Requiring inpatient care',
         '(Ibaraki) Requiring inpatient care',
         '(Tochigi) Requiring inpatient care', '(Gunma) Requiring inpatient care', '(Saitama) Requiring inpatient care',
         '(Chiba) Requiring inpatient care', '(Tokyo) Requiring inpatient care', '(Kanagawa) Requiring inpatient care',
         '(Niigata) Requiring inpatient care', '(Toyama) Requiring inpatient care',
         '(Ishikawa) Requiring inpatient care', '(Fukui) Requiring inpatient care',
         '(Yamanashi) Requiring inpatient care',
         '(Nagano) Requiring inpatient care', '(Gifu) Requiring inpatient care', '(Shizuoka) Requiring inpatient care',
         '(Aichi) Requiring inpatient care', '(Mie) Requiring inpatient care',
         '(Shiga) Requiring inpatient care', '(Kyoto) Requiring inpatient care', '(Osaka) Requiring inpatient care',
         '(Hyogo) Requiring inpatient care', '(Nara) Requiring inpatient care', '(Wakayama) Requiring inpatient care',
         '(Tottori) Requiring inpatient care', '(Shimane) Requiring inpatient care',
         '(Okayama) Requiring inpatient care', '(Hiroshima) Requiring inpatient care',
         '(Yamaguchi) Requiring inpatient care', '(Tokushima) Requiring inpatient care',
         '(Kagawa) Requiring inpatient care', '(Ehime) Requiring inpatient care', '(Kochi) Requiring inpatient care',
         '(Fukuoka) Requiring inpatient care',
         '(Saga) Requiring inpatient care', '(Nagasaki) Requiring inpatient care',
         '(Kumamoto) Requiring inpatient care',
         '(Oita) Requiring inpatient care', '(Miyazaki) Requiring inpatient care',
         '(Kagoshima) Requiring inpatient care',
         '(Okinawa) Requiring inpatient care']]
    df_4.columns = list_prefacture

    df_a = pd.DataFrame()
    df_a[list_data_kind[0]] = df_0[prefacture]
    df_a[list_data_kind[3]] = df_3[prefacture]
    df_a[list_data_kind[4]] = df_4[prefacture]
    df_a[list_data_kind[2]] = df_2[prefacture]
    df_a.index = pd.to_datetime(df_a.index)
    df_a['日時'] = df_a.index.strftime('%Y年%-m月%-d日')

    return df_a


def make_scattergraph(df_b, x_data, y_data, logx, logy):
    #    fig = px.scatter(df_b, x=x_data, y=y_data, color='流行時期', log_x=logx, log_y=logy, trendline="ols")
    fig = px.scatter(df_b, x=x_data, y=y_data, color='流行時期', hover_data=['日時'], log_x=logx, log_y=logy, width=600, height=600, trendline="ols")
    st.plotly_chart(fig, use_container_width=True)


st.set_page_config(layout="wide")
st.title("流行時期ごとの変数関係分析")

with st.sidebar:
    logx = st.checkbox('x軸のログスケール', value=False)
    logy = st.checkbox('y軸のログスケール', value=False)

prefacture = '全国'

dict_data = {
    '新規感染者数': 'newly_confirmed_cases_daily',
    '10万人あたりの新規感染者数': 'newly_confirmed_cases_per_100_thousand_population_daily',
    '重症患者数': 'severe_cases_daily',
    '死亡者数': 'deaths_cumulative_daily',
    '治療必要者数': 'requiring_inpatient_care_etc_daily',
}

list_data_kind = list(dict_data.keys())

list_prefacture = ['全国', '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都',
                   '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府',
                   '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
                   '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

df_a = load_data(prefacture, list_data_kind)
df_b = df_a.dropna(how='any')

dict_start_time = {
    '第1波': '2020-01-01',
    '第2波': '2020-07-10',
    '第3波': '2020-10-01',
    '第4波': '2021-03-25',
    '第5波': '2021-07-15',
    '第6波': '2021-12-10',
    '第7波': '2022-06-15',
}

dict_finish_time = {
    '第1波': '2020-07-10',
    '第2波': '2020-10-01',
    '第3波': '2021-03-25',
    '第4波': '2021-07-15',
    '第5波': '2021-12-10',
    '第6波': '2022-06-15',
    '第7波': df_b.index[-1].to_pydatetime(),
}

for 流行時期 in dict_finish_time.keys():
    mask = (df_b.index >= dict_start_time[流行時期]) & (df_b.index < dict_finish_time[流行時期])
    df_b.loc[mask, '流行時期'] = 流行時期

st.subheader('新規感染者数と日毎死亡者数の比較')
make_scattergraph(df_b, '新規感染者数', '死亡者数', logx, logy)

st.subheader('治療必要者数と重症患者数の比較')
make_scattergraph(df_b, '治療必要者数', '重症患者数', logx, logy)
# make_scattergraph(df_b, '治療必要者数', '死亡者数', logx, logy)
# make_scattergraph(df_b, '重症患者数', '死亡者数', logx, logy)
