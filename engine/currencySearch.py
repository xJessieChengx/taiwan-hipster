import twder

def currencySearch(search):
	dollarTuple = twder.now_all()[search]
	#reply = '{}\n{}的即期賣出價：{}'.format(dollarTuple[0],search,dollarTuple[4])
	reply = '{}\n{}\n現金買入價：{}\n現金賣出價：{}\n即期買入價：{}\n即期賣出價：{}'.format(dollarTuple[0],search,dollarTuple[1],dollarTuple[2],dollarTuple[3],dollarTuple[4])
	return reply