from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.currencySearch import currencySearch #幣值查詢
from engine.AQI import AQImonitor #空氣品質
from engine.gamma import gammamonitor #輻射值
from engine.OWM import OWMLonLatsearch #天氣查詢
from engine.SpotifyScrap import scrapSpotify #Spotify隨機音樂

from engine.KMFA import kaohsiungMuseumOfFineArts
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
        elif userSend == '匯率':
            message = TextSendMessage(text='請輸入正確的英文幣值名稱：')
        elif userSend in ['CNY', 'THB', 'SEK', 'USD', 'IDR', 'AUD', 'NZD', 'PHP', 'MYR', 'GBP', 'ZAR', 'CHF', 'VND', 'EUR', 'KRW', 'SGD', 'JPY', 'CAD', 'HKD']:
            message = TextSendMessage(text=currencySearch(userSend))
        
        #高雄藝文特區
        # elif userSend == '藝文特區':
        #     message = TemplateSendMessage(
        #         alt_text='這是一個按鈕選單',
        #         template=ButtonsTemplate(
        #             thumbnail_image_url='https://www.khcc.gov.tw/PhotoData/PIC1080719.jpg',
        #             title='藝文特區',
        #             text='請選擇地點',
        #             actions=[
        #                 MessageAction(
        #                     label='高雄市立美術館',
        #                     text='高雄市立美術館'
        #                 ),
        #                 MessageAction(
        #                     label='駁二藝術特區',
        #                     text='駁二藝術特區'
        #                 ),
        #                 MessageAction(
        #                     label='高雄文化中心',
        #                     text='高雄文化中心'
        #                 ),
        #                 MessageAction(
        #                     label='高雄市立圖書館總館',
        #                     text='高雄市立圖書館總館'
        #                 ),
        #                 MessageAction(
        #                     label='衛武營國家藝術文化中心',
        #                     text='衛武營國家藝術文化中心'
        #                 )
        #             ]
        #         )
        #     ) 

        elif userSend == '藝文特區':
            message = TemplateSendMessage(
                alt_text='藝文特區',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://yt3.ggpht.com/a/AGF-l7_I5cC4BCgzsjC-KWUtpS67zX9OnaQ6OIv7Sw=s900-c-k-c0xffffffff-no-rj-mo',
                            action=PostbackTemplateAction(
                                label='高雄市立美術館',
                                text='高雄市立美術館',
                                data='action=buy&itemid=1'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://t.kfs.io/upload_images/75049/logo_promote.jpg',
                            action=PostbackTemplateAction(
                                label='駁二藝術特區',
                                text='駁二藝術特區',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://www.taiwan.net.tw/att/1/big_scenic_spots/pic_9285_1.jpg',
                            action=PostbackTemplateAction(
                                label='高雄中正文化中心',
                                text='高雄中正文化中心',
                                data='action=buy&itemid=3'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://images.1111.com.tw/media/share/be/be176ff41da342bd9be476eaaeca1d57.jpg',
                            action=PostbackTemplateAction(
                                label='高雄岡山文化中心',
                                text='高雄岡山文化中心',
                                data='action=buy&itemid=4'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://cdn0.techbang.com/system/images/505989/original/762cbe52aeaf8868c25cf2e6ba95297f.jpg?1552021137',
                            action=PostbackTemplateAction(
                                label='高雄市電影館',
                                text='高雄市電影館',
                                data='action=buy&itemid=5'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://kaohsiungmusichall.khcc.gov.tw/PhotoData/03_1.jpg',
                            action=PostbackTemplateAction(
                                label='高雄市音樂館',
                                text='高雄市音樂館',
                                data='action=buy&itemid=6'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://farm6.staticflickr.com/5607/15414573410_14be148561_o.jpg',
                            action=PostbackTemplateAction(
                                label='大東文化藝術中心',
                                text='大東文化藝術中心',
                                data='action=buy&itemid=7'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://pic.pimg.tw/ksdelicacy/1415936608-3870356857.jpg',
                            action=PostbackTemplateAction(
                                label='高雄市立圖書館總館',
                                text='高雄市立圖書館總館',
                                data='action=buy&itemid=8'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://www.npac-weiwuying.org/assets/images/index/default-cover.jpg',
                            action=PostbackTemplateAction(
                                label='衛武營國家藝術文化中心',
                                text='衛武營國家藝術文化中心',
                                data='action=buy&itemid=9'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://museums.moc.gov.tw/Upload/MuseumDayActivityFrontCover/d093b7a9-72be-48ce-8238-3c08eea58639.jpg',
                            action=PostbackTemplateAction(
                                label='高雄科學工藝博物館',
                                text='高雄科學工藝博物館',
                                data='action=buy&itemid=10'
                            )
                        )
                    ]
                )
            )
        
        #高雄市立美術館
        elif userSend in ['高雄市立美術館','高美館','kaohsiung museum of fine arts','KAOHSIUNG MUSEUM OF FINE ARTS']:
            Museum_Name = '高美館'
            message = TemplateSendMessage(
                alt_text='這是一個按鈕選單',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.kmfa.gov.tw/uploads/07-1810X768.jpg?5791651',
                    title='高雄市立美術館',
                    text='請選擇動作',
                    actions=[
                        MessageAction(
                            label='展覽資訊',
                            text='高雄市立美術館展覽資訊'
                        ),
                        URIAction(
                            label='兒童美術館',
                            uri='https://www.kmfa.gov.tw/Visit/navigation/navigation02.htm'
                        ),
                        URIAction(
                            label='美術館VR環景',
                            uri='https://roundme.com/tour/11129/view/27357/'
                        ),
                        URIAction(
                            label='視覺藝術影像資料庫KMFA',
                            uri='https://www.youtube.com/channel/UC-lj75N-Ojf2iYNTM_Owz9g'
                        )
                    ]
                )
            )
		#高雄市立美術館 #展覽資訊
        elif userSend == '高雄市立美術館展覽資訊':
            data = kaohsiungMuseumOfFineArts()
            message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(columns=data)
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
