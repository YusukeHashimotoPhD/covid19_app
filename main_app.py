import streamlit as st

st.title("covid-19のデータ分析")

text = '''
厚生労働省はcovid-19に関する情報をホームページ上に公開し、毎日更新しています。
https://covid19.mhlw.go.jp/extensions/public/index.html

ここでは、データ科学の手法で公開されたデータを分析していきます。
プログラミングはpythonで執筆し、コードはGitHub上に公開しています。
https://github.com/YusukeHashimotoPhD/covid19_app
'''
st.write(text)
