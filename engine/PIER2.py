import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time
from linebot.models import *

# #整理檔案名稱(展覽名稱)，去除其他特殊符號
# def clearName(name):
# 	newName = ''
# 	for i in name:
# 		if i.isalnum():
# 			newName += i
# 	return newName

# #下載展覽圖片
# def download(link, showname):
# 	image = requests.get('https://pier-2.khcc.gov.tw{}'.format(link))
# 	file = open('{}.jpg'.format(clearName(showname)), mode='wb')
# 	file.write(image.content)
# 	file.close()

#駁二藝術特區
def ThePier2ArtCenter():
	url = 'https://pier-2.khcc.gov.tw/home02.aspx?ID=$3001&IDK=2&EXEC=L'
	headers = {'User-Agent': 'Mozilla/5.0'}
	webContent = requests.get(url, headers=headers)
	webContent.encoding = 'UTF-8'
	soup = BeautifulSoup(webContent.content, 'html.parser')

	#整理檔案名稱(展覽名稱)，去除其他特殊符號
	def clearName(name):
		newName = ''
		for i in name:
			if i.isalnum():
				newName += i
		return newName

		infos = []
		#展覽資訊擷取
		for exhibition in soup.select('.n_box'):
			Name = exhibition.select('.pic img')[0]['alt']
			Date = exhibition.select('.txt')[0].text
			imgLink = exhibition.select('.pic img')[0]['src']
			LinkTemp = exhibition['onclick'].split('=\'')[1]
			Link = LinkTemp[:len(LinkTemp)-1]

			# 測試用
			#infos.append([Name,Date,imgLink])
			if len(infos) < 10:
				infos.append(
					CarouselColumn(
						thumbnail_image_url=imgLink,
						title=Name,
						text=Date,
						actions=[
							URITemplateAction(
								label='展覽資訊',
								uri=Link
							),
							URITemplateAction(
								label='購票連結',
								uri=Link
							)
						]
					)
				)
			else:
				break

		return infos

		# print('展覽名稱：{}'.format(Date))
		# print('展覽圖片：https://pier-2.khcc.gov.tw{}'.format(imgLink))
		# #download(imgLink,Name)
		# print('展覽連結：https://pier-2.khcc.gov.tw/{}'.format(Link))
		# print('------------------------')

	#print('抓取完成')