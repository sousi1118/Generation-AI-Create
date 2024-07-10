import streamlit as st
import pandas as pd
import os
import requests

from openai import OpenAI
client = OpenAI()

st.title("炭酸飲料パッケージジェネレーター")

# エクセルファイルのチェックとクリーンアップを行う関数
def clean_excel(file_path):
    try:
        data = pd.read_excel(file_path)
        if len(data.columns) != 6:
            raise ValueError("エクセルファイルの列数が期待されたものと異なります。")
    except Exception as e:
        st.error(f"エクセルファイルの読み込みエラー: {e}")
        data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume", "design"])
    return data

# エクセルファイルが存在するかチェック、存在しない場合は空のデータフレームを作成してエクセルとして保存
excel_file = "drinks.xlsx"
if not os.path.exists(excel_file):
    data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume", "design"])
    data.to_excel(excel_file, index=False)
else:
    # エクセルファイルをロードしてクリーンアップ
    data = clean_excel(excel_file)

# データの表示
st.write("現在の炭酸飲料データ:")
st.dataframe(data)

# 新しい飲料の入力フォーム
st.header("新しい炭酸飲料の詳細を入力")
product_name = st.text_input("商品名")
description = st.text_input("説明")
taste = st.text_input("味")
volume = st.text_input("容量")
design = st.text_input("デザイン")

if st.button("画像を生成"):
    if product_name and description and taste and volume and design:
        # 画像生成のためのプロンプトを作成
        prompt = (
            f"{data}を参照して"
            f"容量{volume}の{taste}風味の炭酸飲料の画像を作成してください。"
            f"ペットボトルは透明で、中に炭酸の{taste}飲料が見えるようにしてください。"
            f"ラベルは{product_name}の情報を参考にして、{taste}のグラフィックが大胆に描かれ、"
            f"ブランド名{product_name}が上部に目立つように表示されるようにしてください。"
            f"{design}を参照してモダンでリフレッシュ感があり、ペットボトルに水滴がついて冷たさを感じさせるようにしてください。"
            f"背景はシンプルで白にして、ペットボトルに焦点が当たるようにしてください。"
        )

        # OpenAI APIを呼び出して画像を生成
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response.data[0].url
        
        # 生成された画像を保存
        image_response = requests.get(image_url)
        if not os.path.exists("炭酸飲料画像"):
            os.makedirs("炭酸飲料画像")
        file_name = os.path.join("炭酸飲料画像", f"{product_name.replace(' ', '_')}.jpg")
        with open(file_name, 'wb') as f:
            f.write(image_response.content)
        
        # 生成された画像を表示
        st.image(image_url, caption=f"{product_name} パッケージ")

        # 新しいデータをデータフレームに追加
        new_data = pd.DataFrame({
            "file_name": [file_name],
            "product_name": [product_name],
            "description": [description],
            "taste": [taste],
            "volume": [volume],
            "design": [design]
        })
        
        data = pd.concat([data, new_data], ignore_index=True)
        
        # 更新されたデータを保存
        data.to_excel(excel_file, index=False)
        
        st.success("新しい飲料が追加され、画像が生成されました！")
    else:
        st.error("すべてのフィールドに入力してください。")

# 更新されたデータフレームを表示
st.write("更新された炭酸飲料データ:")
st.dataframe(data)
