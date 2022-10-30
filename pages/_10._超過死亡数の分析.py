import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("超過死亡数のデータ分析")

folder_path = './'
file_path = folder_path + 'TimeSeriesResult_20221030155227851.csv'

df = pd.read_csv(file_path)

df['年月'] = pd.to_datetime(df['時点'], format='%Y年%m月')
df['年'] = df['年月'].dt.year
df['月'] = df['年月'].dt.month
df_A = pd.crosstab(index = df['年'], columns = df['月'], values = df['死亡数【人】'], aggfunc = np.mean)

fig = px.imshow(df_A.T,
                title='月毎死亡数の年変化',
                width = 800,
                aspect='auto',
               )
st.plotly_chart(fig, use_container_width=True)

fig = px.imshow(-df_A.diff().T,
                title='月毎死亡数の対前年差',
                width = 800,
                aspect='auto',
                color_continuous_scale=px.colors.sequential.RdBu
               )
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df_A,
              title='月毎死亡数の年変化',
#              x="月",
#              y="死亡数【人】",
#              color = '年'
              )
fig.update_yaxes(title_text='死亡数')
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df_A.diff(),
              title='月毎死亡数の対前年変化',
              )
fig.update_yaxes(title_text='対前年死亡数変化')
st.plotly_chart(fig, use_container_width=True)