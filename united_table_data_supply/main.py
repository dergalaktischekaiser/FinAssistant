from finvizfinance.quote import finvizfinance
from finviz.screener import Screener
import psycopg2 as pz
from datetime import datetime, timezone, timedelta
import time
import json
import requests
import alpha_vantage

# THIS IS ONE OF THE MOST CRUCIAL SCRIPTS IN THE ENTIRE PROJECT.
# WHEN A USER INPUTS A TICKER NAME IN THE STRING FORMAT,
# ALL THE INSERTS, UPDATES AND DIALOGUES WITH THE USER ARE PROCESSING ACCORDING TO THIS SCRIPT.
# MARKET HISTORY IS SAVED AS JSON-VALUE. INTERVAL IS EQUAL TO 5 MINUTES.


def if_row_exists(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # A SELECT PostrgeSQL query which checks whether a row exists or not.
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        cursor.execute("SELECT Company FROM stock_data WHERE Company = %s", (stock_fundament['Company'],))
        connection.commit()
        return cursor.fetchone() is None

    except(Exception, pz.Error) as error:
        print("Connection failed:", error)


def if_row_exists_in_MarketHistory(tckr, comp):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # A SELECT PostrgeSQL query which checks whether a row exists or not.
        # stock = finvizfinance(tckr)
        # stock_fundament = stock.TickerFundament()
        cursor.execute("SELECT stock_name FROM MarketHistory WHERE stock_name = %s", (comp,))
        connection.commit()
        return cursor.fetchone() is None

    except(Exception, pz.Error) as error:
        print("Connection failed:", error)


def insert_data(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        industry = ""
        country = ""
        employees = ""
        volume = ""
        market_cap = ""
        name = stock_fundament['Company']
        tckr = ticker
        sector = stock_fundament['Sector']
        industry = stock_fundament['Industry']
        country = stock_fundament['Country']
        employees = stock_fundament['Employees']
        volume = str(stock_fundament['Volume'])
        market_cap = str(stock_fundament['Market Cap'])
        ptoe = -1.0
        ptob = -1.0
        dividend = -1.0
        dtoe = -1.0
        if type((stock_fundament['P/E'])) != str:
            ptoe = "{:.6f}".format(float(stock_fundament['P/E']))
        if type((stock_fundament['P/B'])) != str:
            ptob = "{:.6f}".format(float(stock_fundament['P/B']))
        if type((stock_fundament['Dividend'])) != str:
            dividend = "{:.6f}".format(float(stock_fundament['Dividend']))
        if type((stock_fundament['Debt/Eq'])) != str:
            dtoe = "{:.6f}".format(float(stock_fundament['Debt/Eq']))
        # A PostrgeSQL query to insert new data.
        insert_query = """INSERT INTO stock_data (Company, Ticker, Sector, Industry,
                       Country, Employees, Volume, Market_Capitalization,
                       PriceToEarnings, PriceToBook, Dividend, DebtToEquity)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        to_insert = (name, tckr, sector, industry, country, employees, volume, market_cap,
                     ptoe, ptob, dividend, dtoe)
        cursor.execute(insert_query, to_insert)
        connection.commit()

    except(Exception, pz.Error) as err:
        print("Connection to stock data failed:", err)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection to stock data closed.\n")


def update_data(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        # A PostgreSQL script which updates the data.
        update_query = """Update stock_data set Company = %s where Company = %s;
                          Update stock_data set Ticker = %s where Company = %s;
                          Update stock_data set Sector = %s where Company = %s;
                          Update stock_data set Industry = %s where Company = %s;
                          Update stock_data set Country = %s where Company = %s;
                          Update stock_data set Employees = %s where Company = %s;
                          Update stock_data set Volume = %s where Company = %s;
                          Update stock_data set Market_Capitalization = %s where Company = %s;
                          Update stock_data set Price = %s where Company = %s;
                          Update stock_data set PriceToEarnings = %s where Company = %s;
                          Update stock_data set PriceToBook = %s where Company = %s;
                          Update stock_data set Dividend = %s where Company = %s;
                          Update stock_data set DebtToEquity = %s where Company = %s;"""
        tckr = ticker
        name_ = stock_fundament['Company']
        sector = stock_fundament['Sector']
        industry = stock_fundament['Industry']
        country = stock_fundament['Country']
        employees = stock_fundament['Employees']
        if (type(employees)) == str:
            employees = -1
        volume = str(stock_fundament['Volume'])
        market_cap = str(stock_fundament['Market Cap'])
        ptoe = -1.0
        ptob = -1.0
        dividend = -1.0
        # dividend = float(stock_fundament['Dividend'])
        dtoe = -1.0
        price = stock_fundament['Price']
        # print((float(stock_fundament['P/E'])))
        # print((stock_fundament['P/E']))
        # print(type(dividend))
        # print(dividend)
        if type((stock_fundament['P/E'])) == str and stock_fundament['P/E'] != '-':
            # if isinstance(stock_fundament['P/E'], float):
            ptoe = (float(stock_fundament['P/E']))
        if type((stock_fundament['P/B'])) == str and stock_fundament['P/B'] != '-':
            ptob = float(stock_fundament['P/B'])
        if type((stock_fundament['Dividend'])) == str and stock_fundament['Dividend'] != '-':
            dividend = float(stock_fundament['Dividend'])
        if type((stock_fundament['Debt/Eq'])) == str and stock_fundament['Debt/Eq'] != '-':
            dtoe = float(stock_fundament['Debt/Eq'])
        to_update = (name_, name_,
                     tckr, name_,
                     sector, name_,
                     industry, name_,
                     country, name_,
                     employees, name_,
                     volume, name_,
                     market_cap, name_,
                     price, name_,
                     ptoe, name_,
                     ptob, name_,
                     dividend, name_,
                     dtoe, name_,)
        cursor.execute(update_query, to_update)
        connection.commit()
        company = name_
        check_history = if_row_exists_in_MarketHistory(ticker, company)
        if not check_history:
            update_hist(ticker, company)
        else:
            insert_hist(ticker, company)

    except(Exception, pz.Error) as err:
        print("Data update failed:", err)

    finally:
        cursor.close()
        connection.close()
        print("Update finished. Connection to stock data closed.\n")


def update_hist(tkr, comp):
    try:
        conn = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cur = conn.cursor()
        link = "https://www.alphavantage.co/query"
        key = "79861QC266FXQM3C"
        link_parameters = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": tkr,
            "interval": "5min",
            "outputsize": "full",
            "apikey": key
        }
        response = requests.get(link, params=link_parameters)
        dict_ = response.json()
        json_object_for_ticker = json.dumps(dict_)
        current_time = datetime.now()
        bundle = (comp, comp, current_time, comp, json_object_for_ticker, comp,)
        upd_query = """UPDATE MarketHistory set stock_name = %s where stock_name = %s;
                       UPDATE MarketHistory set time = %s where stock_name = %s;
                       UPDATE MarketHistory set history = %s where stock_name = %s;"""
        cur.execute(upd_query, bundle)
        conn.commit()
        print("Attention! The company's market history has been updated!\n")

    except(Exception, pz.Error) as exception_:
        print("Something went wrong due to", exception_, '\n')


def insert_hist(tkr, comp):
    try:
        conn = pz.connect(user='yhxvtdvlnvmtxs',
                          password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                          host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                          port='5432',
                          database='d5fre91hfg8vvf')
        cur = conn.cursor()
        link = "https://www.alphavantage.co/query"
        key = "79861QC266FXQM3C"
        link_parameters = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": tkr,
            "interval": "5min",
            "outputsize": "full",
            "apikey": key
        }
        response = requests.get(link, params=link_parameters)
        dict_ = response.json()
        json_object_for_ticker = json.dumps(dict_)
        insert_query = """INSERT INTO MarketHistory (stock_name, time, history)
                          VALUES (%s, %s, %s)"""
        current_time = datetime.now()
        bundle = (comp, current_time, json_object_for_ticker)
        cur.execute(insert_query, bundle)
        conn.commit()
        print("The company's market history has been added!\n")

    except(Exception, pz.Error) as exception_:
        print("Something went wrong due to", exception_, '\n')


def get_data(ticker):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(ticker)
        stock_fundament = stock.TickerFundament()
        tckr = ticker
        name_ = stock_fundament['Company']
        sector = stock_fundament['Sector']
        industry = stock_fundament['Industry']
        country = stock_fundament['Country']
        employees = stock_fundament['Employees']
        volume = str(stock_fundament['Volume'])
        market_cap = str(stock_fundament['Market Cap'])
        ptoe = -1.0
        ptob = -1.0
        dividend = -1.0
        dtoe = -1.0
        if type((stock_fundament['P/E'])) != str:
            ptoe = float(stock_fundament['P/E'])
        if type((stock_fundament['P/B'])) != str:
            ptob = float(stock_fundament['P/B'])
        if type((stock_fundament['Dividend'])) != str:
            dividend = float(stock_fundament['Dividend'])
        if type((stock_fundament['Debt/Eq'])) != str:
            dtoe = float(stock_fundament['Debt/Eq'])
        select_query = """SELECT Company, Ticker, Sector, Industry, Country, 
                          Employees, Volume, Market_Capitalization, Price,
                          PriceToEarnings, PriceToBook, Dividend, DebtToEquity
                          FROM stock_data WHERE Company = %s
                       """
        to_select = (name_,)
        cursor.execute(select_query, to_select)
        data = cursor.fetchone()
        print("==============================================")
        print(tckr)
        print("Company: ", data[0], sep="")
        print("Sector: ", data[2], sep="")
        print("Industry: ", data[3], sep="")
        print("Country: ", data[4], sep="")
        print("Employees: ", data[5], sep="")
        print("Volume: ", data[6], sep="")
        print("Market capitalization: ", data[7], sep="")
        print("Price: ", data[8], sep="")
        print("P/E: ", data[9], sep="")
        print("P/B: ", data[10], sep="")
        print("Dividend: ", data[11], sep="")
        print("D/E: ", data[12], sep="")
        print("==============================================")

    except (Exception, pz.Error) as error:
        print("Getting data failed:", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")


if __name__ == "__main__":
    print("Insert your query:", end=" ")
    ticker_ = input()
    print("...preparing to display...\n")
    try:
        finvizfinance(ticker_)
        print("Ticker found!\n")

    except:
        print("Invalid ticker!\n")
        exit()

    check = if_row_exists(ticker_)
    if not check:
        update_data(ticker_)
    else:
        # insert_data(ticker_)
        print("Ticker not found! Try another one.")
    get_data(ticker_)
    print("\n")
