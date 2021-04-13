from finvizfinance.quote import finvizfinance
# from finviz.screener import Screener
import psycopg2 as pz
from datetime import datetime
import time
import requests
import math

KEYS = [
    "X8XH5CHZVTFQFML6",
    "1257YOCIBS78KNBV",
    "5XMKF8J70OSBSL5D",
    "ECXWLTZIVWCNLSWC"
]
KEYS_ITERATOR = 0
SERIES_15MIN = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=15min&apikey={}"
SERIES_15MIN_PERIOD = 15 * 60
SERIES_15MIN_LAST = 0
SERIES_5MIN = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey={}"
SERIES_5MIN_PERIOD = 5 * 60
SERIES_5MIN_LAST = 0
GOOD_STOCKS = ["AMZN", "GOOGL", "YNDX", "TSLA", "AAPL", "MOMO", "BABA", "BA", "NFLX", "NVDA", "MSFT", "AMGN", "JPM", "FB", "TCS"]
def iterate():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM stock_data"""
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except(Exception, pz.Error) as err:
        print(err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")


def automatic_update():
    while True:
        dt = datetime.utcnow()  # using utc +0 time zone
        h = dt.hour
        if h >= 23:
            time.sleep(28800)
        try:
            connection = pz.connect(user='yhxvtdvlnvmtxs',
                                    password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                    host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                    port='5432',
                                    database='d5fre91hfg8vvf')
            cursor = connection.cursor()
            select_all_query = """SELECT * FROM stock_data"""
            cursor.execute(select_all_query)
            rows = cursor.fetchall()
            upd_query = ""
            print(len(rows))
            for row in rows:
                dt = datetime.utcnow()
                if dt.hour >= 23:
                    break
                ticker = row[1]
                if ticker not in GOOD_STOCKS:
                    continue
                # update(ticker)
                try:
                    stock = finvizfinance(ticker)
                except:
                    print("Ticker not found.")
                    print("Restarting.")
                    continue
                fundament = stock.TickerFundament()
                name = fundament['Company']
                sector = fundament['Sector']
                industry = fundament['Industry']
                country = fundament['Country']
                employees = fundament['Employees']
                if (type(employees)) == str:
                    employees = -1
                volume = str(fundament['Volume'])
                marketcap = str(fundament['Market Cap'])
                ptoe = -1.0
                ptob = -1.0
                dividend = -1.0
                dtoe = -1.0
                price = fundament['Price']
                if type((fundament['P/E'])) == str and fundament['P/E'] != '-':
                    # if isinstance(stock_fundament['P/E'], float):
                    ptoe = float(fundament['P/E'])
                if type((fundament['P/B'])) == str and fundament['P/B'] != '-':
                    ptob = float(fundament['P/B'])
                if type((fundament['Dividend'])) == str and fundament['Dividend'] != '-':
                    dividend = float(fundament['Dividend'])
                if type((fundament['Debt/Eq'])) == str and fundament['Debt/Eq'] != '-':
                    dtoe = float(fundament['Debt/Eq'])
                to_update = (name,
                             ticker,
                             sector,
                             industry,
                             country,
                             employees,
                             volume,
                             marketcap,
                             price,
                             ptoe,
                             ptob,
                             dividend,
                             dtoe,
                             name,)
                upd_query = """Update stock_data set Company = '{}', 
                                                     Ticker = '{}',
                                                     Sector = '{}',
                                                     Industry = '{}',
                                                     Country = '{}',
                                                     Employees = {},
                                                     Volume = '{}',
                                                     Market_Capitalization = '{}',
                                                     Price = {},
                                                     PriceToEarnings = {},
                                                     PriceToBook = {},
                                                     Dividend = {},
                                                     DebtToEquity = {} where Company = '{}';\n"""\
                    .format(name, ticker, sector, industry, country, employees, volume, marketcap, price, ptoe, ptob,
                            dividend, dtoe, name)
                cursor = connection.cursor()
                cursor.execute(upd_query)
                connection.commit()

                if ticker == "AMZN" or ticker == "GOOGL":
                    global KEYS_ITERATOR
                    global SERIES_5MIN_LAST
                    global SERIES_15MIN_LAST
                    now = math.trunc(datetime.utcnow().timestamp())
                    if now - SERIES_5MIN_LAST > SERIES_5MIN_PERIOD:
                        resp = requests.get(SERIES_5MIN.format(ticker, KEYS[KEYS_ITERATOR]))
                        KEYS_ITERATOR = (KEYS_ITERATOR + 1) % len(KEYS)
                        series = resp.json()["Time Series (5min)"]
                        query = "Delete from Stock_To_Chart_Data_5min WHERE stock_name = '{}';\n".format(name)
                        for timestamp, info in series.items():
                            date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                            query += "Insert into Stock_To_Chart_Data_5min(stock_name, open, high, low, close, time) " \
                                     "values('{}', {}, {}, {}, {}, '{}');\n".format(name, info["1. open"], info["2. high"],
                                                                          info["3. low"], info["4. close"], date_time_obj)
                        cursor = connection.cursor()
                        cursor.execute(query)
                        connection.commit()
                        SERIES_5MIN_LAST = now
                        print(ticker, "Chart 5 min updated")

                    if now - SERIES_15MIN_LAST > SERIES_15MIN_PERIOD:
                        resp = requests.get(SERIES_15MIN.format(ticker, KEYS[KEYS_ITERATOR]))
                        KEYS_ITERATOR = (KEYS_ITERATOR + 1) % len(KEYS)
                        series = resp.json()["Time Series (15min)"]
                        query = "Delete from Stock_To_Chart_Data_15min WHERE stock_name = '{}';\n".format(name)
                        for timestamp, info in series.items():
                            date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                            query += "Insert into Stock_To_Chart_Data_15min(stock_name, open, high, low, close, time) " \
                                     "values('{}', {}, {}, {}, {}, '{}');\n".format(name, info["1. open"], info["2. high"],
                                                                          info["3. low"], info["4. close"], date_time_obj)
                        cursor = connection.cursor()
                        cursor.execute(query)
                        connection.commit()
                        SERIES_15MIN_LAST = now
                        print(ticker, "Chart 15 min updated")
                print(ticker, "updated.")

        except(Exception, pz.Error) as err:
            print("Connection terminated:", err)
            print("Restarting...\n")
            continue

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("The table updated.")

automatic_update()
