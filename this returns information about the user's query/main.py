import psycopg2 as pz
# import yfinance as yf
import pandas as pd
from finvizfinance.quote import finvizfinance


def if_row_exists_general_info(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # info = ticker.info
        # query = """select exists(select city from general_information where corp_name = %s)"""
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        cursor.execute("SELECT corp_name FROM general_information WHERE corp_name = %s", (stock_fundament['Company'],))
        connection.commit()
        return cursor.fetchone() is None
    except(Exception, pz.Error) as error:
        print(error)


def if_row_exists_stockmarket(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # _name = ticker.info['longName']
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        _name = stock_fundament['Company']
        cursor.execute("SELECT name FROM stockmarket WHERE name = %s", (_name,))
        return cursor.fetchone() is None
    except(Exception, pz.Error) as error:
        print(error)


def insert_general_info(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # info = ticker.info
        # _name = info['longName']
        # _sector = info['sector']
        # _fte = info['fullTimeEmployees']
        # _phone = info['phone']
        # _ctry = info['country']
        # _city = info['city']
        # insert_query = """INSERT INTO general_information (corp_name, sector, full_time_employees,
        #               phone, country, city) VALUES (%s, %s, %s, %s, %s, %s)"""
        # insert_data = (_name, _sector, _fte, _phone, _ctry, _city)
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        _name = stock_fundament['Company']
        _sector = stock_fundament['Sector']
        _industry = stock_fundament['Industry']
        _country = stock_fundament['Country']
        _empl = stock_fundament['Employees']
        _vlm = stock_fundament['Volume']
        _avgvlm = stock_fundament['Avg Volume']
        insert_query = """INSERT INTO general_information (corp_name, sector, industry, country,
                          employees, volume, averageVolume) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        insert_data = (_name, _sector, _industry, _country, _empl, _vlm, _avgvlm)
        cursor.execute(insert_query, insert_data)
        connection.commit()
        connection.close()
        cursor.close()
        print("Update successful!\n")
        print("The Heroku PostgreSQL connection has been closed.\n\n")

    except(Exception, pz.Error) as error:
        print("Connection terminated due to ", error)


def update_general_info(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # info = ticker.info
        # upd_query = """Update general_information set sector = %s where corp_name = %s;
        #               Update general_information set full_time_employees = %s where corp_name = %s;
        #               Update general_information set phone = %s where corp_name = %s;
        #               Update general_information set country = %s where corp_name = %s;
        #               Update general_information set city = %s where corp_name = %s;"""
        # upd_data = (info['city'], info['longName'])
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        upd_query = """Update general_information set sector = %s where corp_name = %s;
                       Update general_information set industry = %s where corp_name = %s;
                       Update general_information set country = %s where corp_name = %s;
                       Update general_information set employees = %s where corp_name = %s;
                       Update general_information set volume = %s where corp_name = %s;
                       Update general_information set averageVolume = %s where corp_name = %s;"""
        # cursor.execute(upd_query, (info['sector'], info['longName'],
        #                           info['fullTimeEmployees'], info['longName'],
        #                           info['phone'], info['longName'],
        #                           info['country'], info['longName'],
        #                           info['city'], info['longName'],))
        cursor.execute(upd_query, (stock_fundament['Sector'], stock_fundament['Company'],
                                   stock_fundament['Industry'], stock_fundament['Company'],
                                   stock_fundament['Country'], stock_fundament['Company'],
                                   stock_fundament['Employees'], stock_fundament['Company'],
                                   stock_fundament['Volume'], stock_fundament['Company'],
                                   stock_fundament['Avg Volume'], stock_fundament['Company'],))
        connection.commit()
        connection.close()
        cursor.close()
        print("Update of the Heroku database successful!\n")
        print("Connection closed.\n")
    except (Exception, pz.Error) as error:
        print("Update failed because of ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()


def insert_stock_market_for_ticker(ticker):
    print("========AN IMPORTANT ISSUE========")
    print("In this alpha version the most actual data can be from 1 to 7 days old!")
    print("==================================")
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # hist = ticker.history(period=prd)
        # name = ticker.info['longName']
        # openn = "{:.6f}".format(hist['Open'][-1])
        # high = "{:.6f}".format(hist['High'][-1])
        # low = "{:.6f}".format(hist['Low'][-1])
        # close = "{:.6f}".format(hist['Close'][-1])
        # volume = "{:.6f}".format(hist['Volume'][-1])
        # dividends = "{:.6f}".format(hist['Dividends'][-1])
        # insert_query = """INSERT INTO stockmarket (name, open, high,
        #                                          low, close, volume, dividends) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        # insert_data = (name, openn, high, low, close, volume, dividends,)
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        nname = stock_fundament['Company']
        ptoe = "{:.6f}".format(float(stock_fundament['P/E']))
        ptob = "{:.6f}".format(float(stock_fundament['P/B']))
        forwardptoe = "{:.6f}".format(float(stock_fundament['Forward P/E']))
        market_cap = stock_fundament['Market Cap']
        eps_ttm = "{:.6f}".format(float(stock_fundament['EPS (ttm)']))
        eps_nyr = stock_fundament['EPS next Y']
        dividend = "{:.6f}".format(float(stock_fundament['Dividend']))
        dtoe = "{:.6f}".format(float(stock_fundament['Debt/Eq']))
        high52wks = stock_fundament['52W High']
        insert_query = """INSERT INTO stockmarket (name, priceToEarnings, priceToBook, forwardPE,
                          marketCapitalization, earnPerShare_ttm, earnPerShare_nextYear, dividend, debtToEquity,
                          high52wks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_data = (nname, ptoe, ptob, forwardptoe, market_cap, eps_ttm, eps_nyr, dividend, dtoe, high52wks)
        cursor.execute(insert_query, insert_data)
        connection.commit()
    except(Exception, pz.Error) as error:
        print("Connection to the stock market failed due to ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection to stock market data closed.\n")


def update_stock_market_for_ticker(ticker):
    print("========AN IMPORTANT ISSUE========")
    print("In this pre-alpha version the most actual data can be from 1 to 7 days old!")
    print("==================================")
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # _name = ticker.info['longName']
        # hist = ticker.history(period=prd)
        # upd_query = """Update stockmarket set open = %s where name = %s;
        #               Update stockmarket set high = %s where name = %s;
        #               Update stockmarket set low = %s where name = %s;
        #               Update stockmarket set close = %s where name = %s;
        #               Update stockmarket set volume = %s where name = %s;
        #               Update stockmarket set dividends = %s where name = %s;"""
        # cursor.execute(upd_query, ("{:.6f}".format(hist["Open"][-1]), _name,
        #                           "{:.6f}".format(hist["High"][-1]), _name,
        #                           "{:.6f}".format(hist["Low"][-1]), _name,
        #                           "{:.6f}".format(hist["Close"][-1]), _name,
        #                           "{:.6f}".format(hist["Volume"][-1]), _name,
        #                           "{:.6f}".format(hist["Dividends"][-1]), _name,))
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        upd_query = """Update stockmarket set priceToEarnings = %s where name = %s;
                       Update stockmarket set priceToBook = %s where name = %s;
                       Update stockmarket set forwardPE = %s where name = %s;
                       Update stockmarket set marketCapitalization = %s where name = %s;
                       Update stockmarket set earnPerShare_ttm = %s where name = %s;
                       Update stockmarket set earnPerShare_nextYear = %s where name = %s;
                       Update stockmarket set dividend = %s where name = %s;
                       Update stockmarket set debtToEquity = %s where name = %s;
                       Update stockmarket set high52wks = %s where name = %s;"""
        upd_data = ("{:.6f}".format(float(stock_fundament['P/E'])), stock_fundament['Company'],
                    "{:.6f}".format(float(stock_fundament['P/B'])), stock_fundament['Company'],
                    "{:.6f}".format(float(stock_fundament['Forward P/E'])), stock_fundament['Company'],
                    stock_fundament['Market Cap'], stock_fundament['Company'],
                    "{:.6f}".format(float(stock_fundament['EPS (ttm)'])), stock_fundament['Company'],
                    stock_fundament['EPS next Y'], stock_fundament['Company'],
                    "{:.6f}".format(float(stock_fundament['Dividend'])), stock_fundament['Company'],
                    "{:.6f}".format(float(stock_fundament['Debt/Eq'])), stock_fundament['Company'],
                    stock_fundament['52W High'], stock_fundament['Company'],)
        cursor.execute(upd_query, upd_data)
        connection.commit()
    except(Exception, pz.Error) as error:
        print("Stock market update failed due to ", error)
    finally:
        cursor.close()
        connection.close()
        print("Update finished")
        print("Connection to stock market data terminated")


def get_general_info(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # info = ticker.info
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        print("==========================================================================")
        print("GENERAL INFORMATION\n")
        print(stock_fundament['Company'])
        print("Sector: ", stock_fundament['Sector'], sep="")
        print("Industry: ", stock_fundament['Industry'], sep="")
        print("Location: ", stock_fundament['Country'], ",", sep="")
        # print(info['city'])
        # print("Phone: ", info['phone'], sep="")
        print("There are ", stock_fundament['Employees'], " ", "employees ", "in the firm", sep="")
        print("Volume: ", stock_fundament['Volume'], sep="")
        print("Average volume: ", stock_fundament['Avg Volume'], sep="")
        # print("Business field: ", info['sector'], sep="")
    except(Exception, pz.Error) as error:
        print("Data output cancelled because of ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("==========================================================================")


def get_most_actual_stockmarket_data(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        # ptoe = "{:.6f}".format(float(stock_fundament['P/E']))
        # ptob = "{:.6f}".format(float(stock_fundament['P/B']))
        # forwardptoe = "{:.6f}".format(float(stock_fundament['Forward P/E']))
        # market_cap = stock_fundament['Market Cap']
        # eps_ttm = "{:.6f}".format(float(stock_fundament['EPS (ttm)']))
        # eps_nyr = stock_fundament['EPS next Y']
        # dividend = "{:.6f}".format(float(stock_fundament['Dividend']))
        # dtoe = "{:.6f}".format(float(stock_fundament['Debt/Eq']))
        # high52wks = stock_fundament['52W High']
        cursor = connection.cursor()
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        print("==========================================================================")
        print("STOCK MARKET MOST ACTUAL DATA (SEE THE WARNING ABOVE)\n")
        # print(ticker.history(period=prd))
        print("P/E ", "{:.6f}".format(float(stock_fundament['P/E'])), sep="")
        print("P/B ", "{:.6f}".format(float(stock_fundament['P/B'])), sep="")
        print("Forward P/E: ", "{:.6f}".format(float(stock_fundament['Forward P/E'])), sep="")
        print("Market capitalization: ", stock_fundament['Market Cap'], sep="")
        print("EPS (ttm): ", "{:.6f}".format(float(stock_fundament['EPS (ttm)'])), sep="")
        print("EPS (nyr): ", stock_fundament['EPS next Y'], sep="")
        print("Dividend: ", stock_fundament['Dividend'], sep="")
        print("D/E: ", "{:.6f}".format(float(stock_fundament['Debt/Eq'])), sep="")
        print("52 Weeks High: ", stock_fundament['52W High'], sep="")
    except(Exception, pz.Error) as error:
        print("Stock market data output cancelled because of ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("==========================================================================")


print("Type the ticker you are looking for:", end=" ")
ticker = input()
print("...preparing to display...\n")
# tckr = yf.Ticker(ticker)

try:
    # tckr.info
    finvizfinance(ticker)
    print("Ticker found!\n")
except:
    print("Invalid ticker! Try again.\n")
    exit()
check = if_row_exists_general_info(ticker)
if not check:
    update_general_info(ticker)
else:
    insert_general_info(ticker)
get_general_info(ticker)
print("\n")
stock_check = if_row_exists_stockmarket(ticker)
# print("Type the period you would like to observe the firm's stock market data")
# print("Possible periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
# period = input()
if not stock_check:
    update_stock_market_for_ticker(ticker)
else:
    insert_stock_market_for_ticker(ticker)
get_most_actual_stockmarket_data(ticker)
