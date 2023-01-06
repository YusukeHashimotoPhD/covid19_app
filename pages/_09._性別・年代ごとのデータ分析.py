import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("性別・年代ごとのデータ分析")
st.write('左のサイドバーからデータの都道府県と性別が選択できます。データを公表していない都道府県もあるのでご了承ください。')

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

with st.sidebar:
    prefacture = st.selectbox(
        '都道府県名',
        list_prefacture,
        index=0
    )

    sex = st.selectbox(
        '性別',
        ['合計', '男性', '女性'],
        index=0
    )

i = list_prefacture.index(prefacture)

def make_heatmap(label, file_name, i, sex, prefacture, url_1):
    url = url_1 + file_name + '.csv'
    df = pd.read_csv(url, index_col=0)

    # 都道府県のデータを抽出
    df_a = df.iloc[0:, 20 * i:20 + 20 * i]
    df_a.columns = df_a.iloc[0]
    df_b = df_a[1:]
    df_b = df_b.replace('*', '0')
    df_b = df_b.fillna(0)
    df_b = df_b.astype(int)
    if label == '年代別死者数':
        # 累積データから日毎のデータを抽出
        df_b = df_b.diff()
        df_b = df_b.dropna(axis=0)

    # 男性と女性のデータを抽出
    df_man = df_b.iloc[:, 0:10]
    df_woman = df_b.iloc[:, 10:20]

    columns = ['10歳未満', '10代', '20代', '30代', '40代', '50代', '60代', '70代', '80代', '90歳以上']
    df_man.columns = columns
    df_woman.columns = columns

    # 合計データを計算
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

    df_a = df_a.abs()

    st.subheader(f'{prefacture}の{label} （{sex}）')
    fig = px.imshow(df_a.T, aspect="auto")
    fig.update_layout(
        xaxis_title="年代",
        yaxis_title="週",
    )
    st.plotly_chart(fig, use_container_width=True)

    return df_a


def make_barplot(df_s, data_name):
    fig = px.bar(df_s[data_name])
    fig.update_layout(
        title=data_name,
        yaxis_title=data_name,
        xaxis_title="年代",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


url_1 = 'https://covid19.mhlw.go.jp/public/opendata/'

dict_data = {
    '年代別新規陽性者数': 'newly_confirmed_cases_detail_weekly',
    '年代別重症者数': 'severe_cases_detail_weekly',
    '年代別死者数': 'deaths_detail_cumulative_weekly',
}

data_name = '年代別新規陽性者数'
df_new = make_heatmap(data_name, dict_data[data_name], i, sex, prefacture, url_1)
#年齢に強く依存することが示しています。具体的には、新規感染者は若者に集中し、重症者と死者は高齢者に集中しています。このような事実を注視しつつ、効率的かつ効果的な感染対策を行うことが重要だと考えられます。
data_name = '年代別重症者数'
df_severe = make_heatmap(data_name, dict_data[data_name], i, sex, prefacture, url_1)
data_name = '年代別死者数'
df_death = make_heatmap(data_name, dict_data[data_name], i, sex, prefacture, url_1)

list_week = list(df_new.index) + ['合計']

# with st.sidebar:
#     selected_week = st.selectbox(
#         '週',
#         list_week,
#         index=len(df_new)-1
#     )

st.subheader('週ごとの年代別データの比較')

selected_week = st.selectbox(
    '週',
    list_week[::-1],
    index=0
)

df_s = pd.DataFrame()
if selected_week == '合計':
    df_s['年代別新規陽性者数'] = df_new.sum()
    df_s['年代別重症者数'] = df_severe.sum()
    df_s['年代別死者数'] = df_death.abs().sum()
else:
    df_s['年代別新規陽性者数'] = df_new.loc[selected_week]
    df_s['年代別重症者数'] = df_severe.loc[selected_week]
    df_s['年代別死者数'] = df_death.loc[selected_week].abs()

#st.subheader(selected_week + '　年代別データの比較')


col0, col1, col2 = st.columns(3)

with col0:
    make_barplot(df_s, '年代別新規陽性者数')
with col1:
    make_barplot(df_s, '年代別重症者数')
with col2:
    make_barplot(df_s, '年代別死者数')

st.caption('新規感染者は若者に集中し、重症者と死者は高齢者に集中していることがわかります。')

st.write('データソース')
url = url_1 + dict_data['年代別新規陽性者数'] + '.csv'
st.caption(f'年代別新規陽性者数: {url}')

url = url_1 + dict_data['年代別重症者数'] + '.csv'
st.caption(f'年代別重症者数: {url}')

url = url_1 + dict_data['年代別死者数'] + '.csv'
st.caption(f'年代別死者数: {url}')
