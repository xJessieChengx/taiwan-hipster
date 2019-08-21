import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time

#def KaohsiungMuseum():
#高美館展覽
url = 'https://www.kmfa.gov.tw/ExhibitionListC001100.aspx'
headers = {'User-Agent': 'Mozilla/5.0'}
webContent = requests.get(url, headers=headers)
webContent.encoding = 'UTF-8'
soup = BeautifulSoup(webContent.content, 'html.parser')
#soup = BeautifulSoup(webContent.text, 'html.parser')

#展覽資訊擷取
for exhibition in soup.select('.exhibition_list .exhibition_item'):
	Name = exhibition.select('.exhibition_title')[0].text
	Date = exhibition.select('.exhibition_date')[0].text
	ImgLink = exhibition.select('img')[0]['src']
	for exhibition in soup.select('.exhibition_list'):
			Link = exhibition.select('a')[0]['href']

	print('展覽名稱：{}'.format(Name))
	print('展覽日期：{}'.format(Date))
	print('展覽圖片：https://www.kmfa.gov.tw/{}'.format(ImgLink))
	print('展覽連結：https://www.kmfa.gov.tw{}'.format(Link))
	print('------------------------')

#下載展覽圖片 
items = soup.find_all('.exhibition_list .exhibition_item img')
folder_path = './photo/'
if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
    os.makedirs(folder_path)  # 创建文件夹
 
for index,item in enumerate(items):
	if item:		
		html = requests.get(item.get('https://www.kmfa.gov.tw/{}'.format(ImgLink)))   # get函数获取图片链接地址，requests发送访问请求
		img_name = folder_path + str(index + 1) +'.jpg'
		with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
			file.write(html.content)
			file.flush()
		file.close()
		print('第%d张图片下载完成' %(index+1))
		time.sleep(1)
print('抓取完成')