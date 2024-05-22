##チャットボットの作成
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# データベースの読み込み
df = pd.read_csv('drinks.csv')

@app.route('/generate_label', methods=['POST'])
def generate_label():
    data = request.json
    product_name = data.get('product_name')
    
    if product_name not in df['product_name'].values:
        return jsonify({"error": "Product not found"}), 404
    
    product_info = df[df['product_name'] == product_name].iloc[0]
    label = {
        "product_name": product_info['product_name'],
        "description": product_info['description'],
        "ingredients": product_info['ingredients'],
        "volume": product_info['volume']
    }
    
    return jsonify(label)

if __name__ == '__main__':
    app.run(debug=True)

##ラベル情報の生成
import requests

url = 'http://127.0.0.1:5000/generate_label'
data = {
    "product_name": "キリンレモン"
}

response = requests.post(url, json=data)
print(response.json())    