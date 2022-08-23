import streamlit as st
import pandas as pd

df = pd.DataFrame()

st.write('start')

df.to_csv('./tempDir/test.csv')

st.write('data is saved')