import streamlit as st
import pandas as pd
import os

# CSVファイルを読み込む
@st.cache_data
def load_data():
    return pd.read_csv("drinks.csv")

# データの読み込み
data = load_data()

# タイトル
st.title("エナジードリンク情報表示")

# デバッグ情報を表示
st.write("CSVファイルの内容:")
st.dataframe(data)

# セレクトボックスで商品名を選択
product_name = st.selectbox("商品名を選択してください", data['product_name'])

# 選択した商品名のデータを表示
if product_name:
    selected_data = data[data['product_name'] == product_name]
    st.write("選択した商品名の内容:")
    st.dataframe(selected_data)

    # 画像の表示
    image_folder = "炭酸飲料画像"
    file_name = selected_data['file_name'].values[0]  # assuming there is a column named 'file_name'
    image_path = os.path.join(image_folder, file_name)  # assuming the file_name matches the image file name
    if os.path.exists(image_path):
        st.image(image_path, caption=product_name)
    else:
        st.write("画像が見つかりませんでした")
