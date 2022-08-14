import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("都道府県ごとのデータ分析")
st.caption('厚生労働省が発表したデータをグラフ化しています。 https://covid19.mhlw.go.jp/extensions/public/index.html')

dict_data = {
    '新規感染者数': 'newly_confirmed_cases_daily',
    '10万人あたりの新規感染者数': 'newly_confirmed_cases_per_100_thousand_population_daily',
    '重症患者数': 'severe_cases_daily',
    '死亡者数': 'deaths_cumulative_daily',
    '治療必要者数': 'requiring_inpatient_care_etc_daily',
}

list_prefacture = ['全国', '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都',
                   '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府',
                   '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
                   '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
list_data_kind = list(dict_data.keys())

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
     '(Ishikawa) Requiring inpatient care', '(Fukui) Requiring inpatient care', '(Yamanashi) Requiring inpatient care',
     '(Nagano) Requiring inpatient care', '(Gifu) Requiring inpatient care', '(Shizuoka) Requiring inpatient care',
     '(Aichi) Requiring inpatient care', '(Mie) Requiring inpatient care',
     '(Shiga) Requiring inpatient care', '(Kyoto) Requiring inpatient care', '(Osaka) Requiring inpatient care',
     '(Hyogo) Requiring inpatient care', '(Nara) Requiring inpatient care', '(Wakayama) Requiring inpatient care',
     '(Tottori) Requiring inpatient care', '(Shimane) Requiring inpatient care',
     '(Okayama) Requiring inpatient care', '(Hiroshima) Requiring inpatient care',
     '(Yamaguchi) Requiring inpatient care', '(Tokushima) Requiring inpatient care',
     '(Kagawa) Requiring inpatient care', '(Ehime) Requiring inpatient care', '(Kochi) Requiring inpatient care',
     '(Fukuoka) Requiring inpatient care',
     '(Saga) Requiring inpatient care', '(Nagasaki) Requiring inpatient care', '(Kumamoto) Requiring inpatient care',
     '(Oita) Requiring inpatient care', '(Miyazaki) Requiring inpatient care', '(Kagoshima) Requiring inpatient care',
     '(Okinawa) Requiring inpatient care']]
df_4.columns = list_prefacture

with st.sidebar:
    prefacture = st.selectbox(
        '都道府県名',
        list_prefacture,
        index=13
    )

    sex = st.selectbox(
        '性別',
        ['合計', '男性', '女性'],
        index=0
    )

i = list_prefacture.index(prefacture)

# st.write(prefacture)

df_a = pd.DataFrame()
df_a[list_data_kind[0]] = df_0[prefacture]
df_a[list_data_kind[3]] = df_3[prefacture]
df_a[list_data_kind[4]] = df_4[prefacture]
df_a[list_data_kind[2]] = df_2[prefacture]
df_a.index = pd.to_datetime(df_a.index)

fig = px.line(df_a[[list_data_kind[0], list_data_kind[3]]])
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
    title=f'{list_data_kind[0]}と{list_data_kind[3]}の時系列データ（日毎）',
    yaxis_title=f'{list_data_kind[0]}と{list_data_kind[3]}',
    xaxis_title="日時",
    #    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df_a[[list_data_kind[4], list_data_kind[2]]])
fig.update_xaxes(tickformat="%Y年%m月")
fig.update_layout(
    title=f'{list_data_kind[4]}と{list_data_kind[2]}の時系列データ（集計）',
    yaxis_title=f'{list_data_kind[2]}と{list_data_kind[4]}',
    xaxis_title="日時",
    #    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('左のサイドバーから、データの性別が選択できます。')

def make_heatmap(label, file_name, i, sex, prefacture):
    url = url_1 + file_name + '.csv'
    df = pd.read_csv(url, index_col=0)
    df_a = df.iloc[0:, 20 * i:20 + 20 * i]
    df_a.columns = df_a.iloc[0]
    df_b = df_a[1:]
    df_b = df_b.replace('*', '0')
    df_b = df_b.fillna(0)
    df_b = df_b.astype(int)
    if label == '年代別死者数':
        df_b = df_b.diff()
        df_b = df_b.dropna(axis=0)

    df_man = df_b.iloc[:, 0:10]
    df_woman = df_b.iloc[:, 10:20]

    columns = ['10歳未満', '10代', '20代', '30代', '40代', '50代', '60代', '70代', '80代', '90歳以上']
    df_man.columns = columns
    df_woman.columns = columns

    df_total = df_man.copy()
    for i in range(df_man.shape[0]):
        for j in range(df_man.shape[1]):
            df_total.iloc[i, j] = df_man.iloc[i, j] + df_woman.iloc[i, j]

    if sex == '男性':
        df_a = df_man
    elif sex == '女性':
        df_a = df_woman
    else:
        df_a = df_total

    fig = px.imshow(df_a, aspect="auto", height=600)
    fig.update_layout(
        title=f'{prefacture}の{label} （{sex}）',
        xaxis_title="年代",
        yaxis_title="週",
    )
    st.plotly_chart(fig, use_container_width=True)


make_heatmap('年代別新規陽性者数', 'newly_confirmed_cases_detail_weekly', i, sex, prefacture)
make_heatmap('年代別重症者数', 'severe_cases_detail_weekly', i, sex, prefacture)
make_heatmap('年代別死者数', 'deaths_detail_cumulative_weekly', i, sex, prefacture)
