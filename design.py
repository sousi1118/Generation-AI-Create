from openai import OpenAI
import base64

# OpenAIクライアントを初期化する
client = OpenAI()

# 画像をbase64文字列にエンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 画像のパス
image_path = "炭酸飲料画像/51EWaAkVoOL._AC_SL1200_.jpg"

# 画像のbase64エンコードされた文字列を取得する
base64_image = encode_image(image_path)

# base64エンコードされた画像を含むメッセージを作成する
prompt = "デザインコンセプト: 商品名のパッケージデザインを説明してください。このドリンクは、ターゲットオーディエンスに向けたもので、フレーバーや成分の特長を反映しています。パッケージのカラー、ロゴ、テキスト、グラフィック、全体のレイアウトなどの視覚的要素を詳細に記述してください。以下の点を含めてください：\n\nカラー: パッケージに使用されている主な色とその意味。\nロゴ: ロゴのデザイン、配置、およびその視覚的な印象。\nテキスト: 商品名、キャッチフレーズ、成分表示など、パッケージに記載されているテキストの内容とフォントスタイル。\nグラフィック: パッケージに描かれているイラスト、模様、シンボルなどの視覚的要素。\n全体のレイアウト: 上記の要素がどのように配置され、パッケージ全体としてどのような印象を与えるか。\n具体的なデザインの例やインスピレーション源も挙げて、デザインの背景や意図を説明してください。"

message_content = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': prompt
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url':  f"data:image/jpeg;base64,{base64_image}"
                    }
                },
            ]
        },
    ]

# ChatCompletions APIを呼び出す
response = client.chat.completions.create(
    model="gpt-4o",
    messages=message_content
)

# ChatCompletions APIからの結果を表示する
print(response.choices[0].message.content)

