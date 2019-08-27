import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time
from linebot.models import *

#下載展覽圖片
# def download(link, showname):
# 	image = requests.get('https://www.kmfa.gov.tw/{}'.format(link))
# 	file = open('{}.jpg'.format(showname), mode='wb')
# 	file.write(imag/e.content)
# 	file.close()

#下載展覽圖片放置資料夾 
# folder_path = './kmfa-photo/'
# if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
#     os.makedirs(folder_path)  # 创建文件夹

#高雄美術館
def kaohsiungMuseumOfFineArts():
	url = 'https://www.kmfa.gov.tw/ExhibitionListC001100.aspx'
	headers = {'User-Agent': 'Mozilla/5.0'}
	webContent = requests.get(url, headers=headers)
	webContent.encoding = 'UTF-8'
	soup = BeautifulSoup(webContent.content, 'html.parser')

	infos = []
	#展覽資訊擷取
	for exhibition in soup.select('.exhibition_list .exhibition_item'):
		Name = exhibition.select('.exhibition_title')[0].text
		Date = exhibition.select('.exhibition_date')[0].text
		ImgLink = exhibition.select('img')[0]['src']
		for exhibition in soup.select('.exhibition_list'):
			Link = exhibition.select('a')[0]['href']
		
		# 測試用
		infos.append([Name,Date,ImgLink])

		CarouselColumn(
			thumbnail_image_url='https://www.kmfa.gov.tw/{}'.format(ImgLink),
			title=Name,
			text=Date,
			actions=[
				URITemplateAction(
					label='展覽資訊',
					uri='https://www.kmfa.gov.tw{}'.format(Link)
				),
				URITemplateAction(
					label='展覽資訊',
					uri='https://www.kmfa.gov.tw{}'.format(Link)
				)
			]
		)
		if len(infos)<10:
			infos.append(CarouselColumn) 
		else:
			break      

	return infos
		# print('展覽名稱：{}'.format(Name))
		# print('展覽日期：{}'.format(Date))
		# print('展覽圖片：https://www.kmfa.gov.tw/{}'.format(ImgLink))
		# #download(ImgLink,Name)
		# print('展覽連結：https://www.kmfa.gov.tw{}'.format(Link))
		# print('------------------------')

#print('抓取完成')
print(kaohsiungMuseumOfFineArts())