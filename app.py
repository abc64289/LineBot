from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設置 Line 機器人的 Channel access token 和 Channel secret
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 處理來自 Line 的訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # 取得請求的內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 收到的訊息
    received_message = event.message.text
    
    # 如果收到訊息是 "1"，則回覆 "2"
    if received_message == "1":
        reply_message = "2"
    else:
        reply_message = "你說了：" + received_message
    
    # 回覆訊息給使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()
