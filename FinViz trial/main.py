import pandas as pd
from finvizfinance.quote import finvizfinance
from finvizfinance.screener.overview import Overview

stock = finvizfinance('tsla')
stock.TickerCharts()
stock_fundament = stock.TickerFundament()
# print(stock_fundament)
for elem in stock_fundament:
    print(elem, stock_fundament[elem], "\n")
