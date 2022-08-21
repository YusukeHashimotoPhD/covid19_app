import streamlit as st

st.title("covid-19のデータ分析")

text = '''
厚生労働省はcovid-19に関する情報をホームページ上に公開し、毎日更新しています。\n
https://covid19.mhlw.go.jp/extensions/public/index.html

ここでは、データ科学の手法で公開されたデータをグラフかし、簡単な分析をしています。

データの表示\n
　時系列データの表示\n
　都道府県別日毎データの表示\n
　クラスタ発生状況の表示\n

データ分析\n
　都道府県別データの分析\n
　期間抽出データの分析\n
　流行時期ごとのデータ分析\n
　性別・年代ごとのデータ分析\n

プログラミングはpythonで執筆し、コードはGitHub上に公開しています。\n
https://github.com/YusukeHashimotoPhD/covid19_app
'''
st.write(text)

st.caption('免責事項：　本アプリによって生じたいかなる問題に対しても責任を負いません。自己責任での利用をお願いいたします。')