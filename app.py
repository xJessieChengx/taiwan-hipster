from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.currencySearch import currencySearch #幣值查詢
from engine.AQI import AQImonitor #空氣品質
from engine.gamma import gammamonitor #輻射值
from engine.OWM import OWMLonLatsearch #天氣查詢
from engine.SpotifyScrap import scrapSpotify #Spotify隨機音樂
#from engine.bookingSystem import booking
#from engine.movie import getMoviePoster
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Okinawa.json',scope)

#儲存資料至Google試算表
client = gspread.authorize(creds)
LineBotSheet = client.open('TaiwanHipsterLineBot')
userStatusSheet = LineBotSheet.worksheet('userStatus')
userInfoSheet = LineBotSheet.worksheet('userInfo')
#movieInfoSheet = LineBotSheet.worksheet('movie')

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

@app.route("/web")
def showWeb():
    return '<h1>Hello Every one</h1>'

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容

#使用者註冊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print('執行TextMessage')
    userSend = event.message.text
    userID = event.source.user_id
    try:
        cell = userStatusSheet.find(userID)
        userRow = cell.row
        userCol = cell.col
        status = userStatusSheet.cell(cell.row,2).value
    except:
        userStatusSheet.append_row([userID])
        userInfoSheet.append_row([userID])
        cell = userStatusSheet.find(userID)
        userRow = cell.row
        userCol = cell.col
        status = ''
    if status == '':
        message = TextSendMessage(text='請輸入姓名, 讓我認識你!')
        userStatusSheet.update_cell(userRow, 2, '註冊中')
    elif status == '註冊中':
        userInfoSheet.update_cell(userRow, 2, userSend)
        userStatusSheet.update_cell(userRow, 2, '已註冊')
        message = TextSendMessage(text='Hi,{}'.format(userSend))
    elif status == '已註冊':
        if userSend == '你好':
            userName = userInfoSheet.cell(cell.row,2).value
            message = TextSendMessage(text='Hello, ' + userName + '已註冊成功!')

        #天氣查詢
        elif userSend == '天氣':
            userStatusSheet.update_cell(userRow, 2, '天氣查詢')
            message = TemplateSendMessage(
				alt_text='請點選位置資訊來傳送',
				template=ConfirmTemplate(
					text='是否傳送位置資訊？',
					actions=[
						URIAction(
							label='傳送',
							uri='line://nv/location'
						),
						PostbackAction(
							label='取消',
							data='取消查詢'
						)
					]
				)
        	)

        #幣值查詢
        elif userSend in ['CNY', 'THB', 'SEK', 'USD', 'IDR', 'AUD', 'NZD', 'PHP', 'MYR', 'GBP', 'ZAR', 'CHF', 'VND', 'EUR', 'KRW', 'SGD', 'JPY', 'CAD', 'HKD']:
            message = TextSendMessage(text=currencySearch(userSend))


        #高雄展覽快訊
        #elif userSend == '展覽快訊':
            
        #高雄藝文特區
        elif userSend == '藝文特區':
            message = TemplateSendMessage(
                alt_text='這是一個按鈕選單',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.khcc.gov.tw/PhotoData/PIC1080719.jpg',
                    title='藝文特區',
                    text='請選擇動作',
                    actions=[
                        URIAction(
                            label='高雄市立美術館',
                            uri='https://www.kmfa.gov.tw/ExhibitionListC001100.aspx?'
                        ),
                        URIAction(
                            label='高雄駁二藝術特區',
                            uri='https://pier-2.khcc.gov.tw/home02.aspx?'
                        ),
                        URIAction(
                            label='衛武營國家藝術文化中心',
                            uri='https://www.npac-weiwuying.org/programs'
                        )
                    ]
                )
            ) 
    
        #高雄市立美術館
        elif userSend == '高美館':
            message = TemplateSendMessage(
                alt_text='這是一個按鈕選單',
                template=ButtonsTemplate(
                    thumbnail_image_url='http://www.kaho.tw/images/pic1.jpg',
                    title='高雄市立美術館',
                    text='請選擇動作',
                    actions=[
                        URIAction(
                            label='展覽資訊',
                            uri='https://www.kmfa.gov.tw/ExhibitionListC001100.aspx?'
                        ),
                        URIAction(
                            label='兒童美術館',
                             uri='https://www.kmfa.gov.tw/Visit/navigation/navigation02.htm'
                        ),
                        URIAction(
                            label='美術館VR環景',
                            uri='https://roundme.com/tour/11129/view/27357/'
                        )
                    ]
                )
            )
        #spotify音樂推薦
        elif userSend in ['spotify','音樂','music']:
            columnReply,textReply = scrapSpotify()
            message = TemplateSendMessage(
                alt_text=textReply,
                template=ImageCarouselTemplate(
                    columns=columnReply
                )
            )
        else:
            message = TextSendMessage(text=userSend) #應聲蟲
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
	userSend = event.message.text
	userID = event.source.user_id
	try:
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = userStatusSheet.cell(cell.row,2).value
	except:
		userStatusSheet.append_row([userID])
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = ''
	if status == '天氣查詢':
		userAddress = event.message.address
		userLat = event.message.latitude
		userLon = event.message.longitude

		weatherResult = OWMLonLatsearch(userLon,userLat)
		AQIResult = AQImonitor(userLon,userLat)
		gammaResult = gammamonitor(userLon,userLat)
		userStatusSheet.update_cell(userRow, 2, '已註冊')
		message = TextSendMessage(text='🌤天氣狀況：\n{}\n🚩空氣品質：\n{}\n\n🌌輻射值：\n{}'.format(weatherResult,AQIResult,gammaResult))
	else:
		message = TextSendMessage(text='傳地址幹嘛?')
	line_bot_api.reply_message(event.reply_token, message)


#回覆貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    print('執行StickerMessage')
    message = TextSendMessage(text='嗚嗚~我看不懂貼圖')
    line_bot_api.reply_message(event.reply_token, message)

#隱藏資訊
@handler.add(PostbackEvent)
def handle_message(event):
	send = event.postback.data
	userID = event.source.user_id
	try:
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = userStatusSheet.cell(cell.row,2).value
	except:
		userStatusSheet.append_row([userID])
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		userCol = cell.col
		status = ''
	if send == '取消查詢':
		reply = '已經取消查詢'
		userStatusSheet.update_cell(userRow, 2, '已註冊')
		message = TextSendMessage(text=reply)
	line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
