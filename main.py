import streamlit as st
import openai
import pandas as pd
import os
import requests

st.title("炭酸飲料パッケージジェネレーター")

# CSVファイルのチェックとクリーンアップを行う関数
def clean_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        if len(data.columns) != 5:
            raise ValueError("CSVファイルの列数が期待されたものと異なります。")
    except pd.errors.ParserError as e:
        st.error(f"CSVファイルの読み込みエラー: {e}")
        with open(file_path, 'r') as f:
            content = f.readlines()
        st.text("CSVファイルの内容（最初の50行）:")
        st.text("".join(content[:50]))  # CSVファイルの最初の50行を表示
        data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    except Exception as e:
        st.error(f"予期せぬエラー: {e}")
        data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    return data

# CSVファイルが存在するかチェック、存在しない場合は空のデータフレームを作成してCSVとして保存
csv_file = "drinks.csv"
if not os.path.exists(csv_file):
    data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    data.to_csv(csv_file, index=False)
else:
    # CSVファイルをロードしてクリーンアップ
    data = clean_csv(csv_file)

# データの表示
st.write("現在の炭酸飲料データ:")
st.dataframe(data)

# 新しい飲料の入力フォーム
st.header("新しい炭酸飲料の詳細を入力")
product_name = st.text_input("商品名")
description = st.text_input("説明")
taste = st.text_input("味")
volume = st.text_input("容量")

if st.button("画像を生成"):
    if product_name and description and taste and volume:
        # 画像生成のためのプロンプトを作成
        prompt = (
            f"容量{volume}の{taste}風味の炭酸飲料の画像を作成してください。"
            f"ボトルは透明で、中に炭酸の{taste}飲料が見えるようにしてください。"
            f"ラベルは{product_name}の情報を参考にして、{taste}のグラフィックが大胆に描かれ、"
            f"ブランド名{product_name}が上部に目立つように表示されるようにしてください。"
            f"デザインはモダンでリフレッシュ感があり、ボトルに水滴がついて冷たさを感じさせるようにしてください。"
            f"背景はシンプルで白にして、ボトルに焦点が当たるようにしてください。"
        )

        # OpenAI APIを呼び出して画像を生成
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response['data'][0]['url']
        
        # 生成された画像を保存
        image_response = requests.get(image_url)
        file_name = f"{product_name.replace(' ', '_')}.jpg"
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
            "volume": [volume]
        })
        
        data = data.append(new_data, ignore_index=True)
        
        # 更新されたデータを保存
        data.to_csv(csv_file, index=False)
        
        st.success("新しい飲料が追加され、画像が生成されました！")
    else:
        st.error("すべてのフィールドに入力してください。")

# 更新されたデータフレームを表示（任意）
st.write("更新された炭酸飲料データ:")
st.dataframe(data)
