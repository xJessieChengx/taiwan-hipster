import twder

def currencySearch(search):
	dollarTuple = twder.now_all()[search]
	reply = '{}\n{}的即期賣出價：{}'.format(dollarTuple[0],search,dollarTuple[4])
	return reply