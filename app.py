from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.currencySearch import currencySearch
from engine.AQI import AQImonitor
from engine.gamma import gammamonitor
from engine.OWM import OWMLonLatsearch
from engine.SpotifyScrap import scrapSpotify
from engine.bookingSystem import booking
from engine.movie import getMoviePoster
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

# 設定你的Channel Access Token
line_bot_api = LineBotApi('zmKGAVHcvWO7gulnFT/doUVRNOLOaA4jff666c869pZ3v5Q6m3h7bvcg8HyvJr+cCP1WsWeNuN1Qtn29yqtsSw44IFnr3osgx0Bw3JhwWs6fJQQ0J18yGRWOTqDG0Z5oz0A3j8rK4ZUYjukLF0ysgQdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('2a88e68deabce9366a4e0e6b995c71e6')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容

#回覆貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    print('執行StickerMessage')
    message = TextSendMessage(text='嗚嗚~我看不懂貼圖')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
