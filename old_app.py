
from flask import Flask, request, abort
from pathlib import Path
import requests
# os内のenvironmentを扱うライブラリ
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FileMessage, TextSendMessage,
)



#環境変数取得

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
LINE_CONTENT_URL = 'https://api.line.me/v2/bot/message/{message_id}/content'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


app = Flask(__name__)



@app.route("/")
def hello_world():
    return "hello!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=FileMessage)
def handle_message(event):
    # メッセージがファイルの場合
    if event.message.type == 'file':
        file_message_id = event.message.id
        download_file(file_message_id)
        import os
        path = f'./files/{file_message_id}.pdf'
        p = Path(path)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(p.resolve()))
        )

def download_file(file_message_id):
    # Line Messaging APIのファイル取得エンドポイントのURLを構築
    url = LINE_CONTENT_URL.format(message_id=file_message_id)

    # Line Messaging APIに対してGETリクエストを送信
    response = requests.get(url, headers={'Authorization': f'Bearer {YOUR_CHANNEL_ACCESS_TOKEN}'})

    # レスポンスのステータスコードが200の場合、ファイルを保存
    if response.status_code == 200:
        with open(f'/code/files/{file_message_id}.pdf', 'wb') as file:
            file.write(response.content)
            print('File downloaded successfully')

if __name__ == "__main__":
    app.run()
