import requests
from bs4 import BeautifulSoup

url = 'http://event.moc.gov.tw/dailyEventRSS2016.asp?mp={}'
webContent = requests.get(url)
#print(webContent.text)

soup = BeautifulSoup(webContent.text,'lxml')

for corporation in soup.select('Rvlmd'):
	print(corporation.find('corporation_name').text)
	try:
		print(corporation.find('contact_no').text)
		print(corporation.find('corporation_address').text)
		print(corporation.find('gpa101_caluse').text)
	except:
		pass
	print('------------------------------------')