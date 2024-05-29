import streamlit as st
import pandas as pd

# CSVファイルの読み込み
csv_file = 'drinks.csv'  # CSVファイルのパス
df = pd.read_csv(csv_file)

# アプリケーションのタイトル
st.title('Drink Label Generator')

# サイドバーに新しいラベル情報を入力するフォームを作成
st.sidebar.header('Create a New Label')
product_name = st.sidebar.text_input('Product Name')
description = st.sidebar.text_input('Description')
taste = st.sidebar.text_input('Taste')
volume = st.sidebar.text_input('Volume')

# サイドバーのボタンを押して新しいラベルを追加
if st.sidebar.button('Add New Label'):
    new_label = {
        'product_name': product_name,
        'description': description,
        'taste': taste,
        'volume': volume
    }
    df = df.append(new_label, ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.sidebar.success('New label added successfully!')

# 既存のラベルを選択して表示
st.header('Existing Labels')
selected_product = st.selectbox('Select a product', df['product_name'].unique())

if selected_product:
    product_info = df[df['product_name'] == selected_product].iloc[0]
    st.subheader(f'Label for {selected_product}')
    st.text(f"Description: {product_info['description']}")
    st.text(f"Taste: {product_info['taste']}")
    st.text(f"Volume: {product_info['volume']}")

# 全てのラベルを表示
st.header('All Labels')
st.dataframe(df)