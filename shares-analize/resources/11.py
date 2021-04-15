











from finvizfinance.quote import finvizfinance
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
stock = finvizfinance('tsla+amzn')
fund = stock.TickerFundament()
print(fund)
#print("{:.6f}".format(float(fund["P/E"])))
#print("aaaaaa")

