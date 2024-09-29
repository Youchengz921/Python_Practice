from flask import Flask, request
import json

# 使用舊版的 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        access_token = 'S5BTlHvuAVYpzTjhvB2he0tqN0FhTFiXLFNB4FS8hc/2V52o/23yxnem0sl0jaRvWVuLzSvZ6J4HK/WAfo98qfw2UaVYNRNQPId8E0P+NQc5hvUjSij4G9S6RRhv/d5bvLpTctWdEQFnCbbsmtVlEQdB04t89/1O/w1cDnyilFU='
        secret = 'e1add7ccc607c4671aa030a58f038039'
        
        # 暫時使用舊版的 LineBotApi 和 WebhookHandler
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        
        tk = json_data['events'][0]['replyToken']
        msg_type = json_data['events'][0]['message']['type']
        
        if msg_type == 'text':
            msg = json_data['events'][0]['message']['text']
            print(msg)
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        
        line_bot_api.reply_message(tk, TextSendMessage(text=reply))
        
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel secret/access token.")
    except Exception as e:
        print(f"Error: {e}")

    return 'OK'

if __name__ == "__main__":
    app.run()
