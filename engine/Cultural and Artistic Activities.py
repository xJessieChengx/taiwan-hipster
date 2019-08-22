import requests
import json

# file = open('scenic_spot_C_f.json', mode='r', encoding='UTF-8-sig')
# data = json.load(file)
URL = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=6'
r = requests.get(URL).json()
#userInput = ''

for show in data['Info']:
	print('展覽名稱：{}'.format(show['title']))
	print('展覽地點：{}'.format(show['locationName']))
	print('展覽地址：{}'.format(show['location']))
	print('展覽時間：{}'.format(show['showInfo']['time'] + '~' + ['endTime']))
	print('展覽票價：{}'.format(show['price'])
		
	print('------------------')