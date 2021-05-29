from flask import Flask, render_template
from flask import request, escape
from finvizfinance.quote import finvizfinance
from finviz.screener import Screener
import psycopg2 as pz
from datetime import datetime, timezone, timedelta
import time
import json
import requests
import alpha_vantage
import os

app = Flask(__name__)

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

# @app.route("/")
# def home():
#     return render_template('bck1.html')
picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route("/h")
def db_pic():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'db.jpg')
    return render_template("back1.html", user_image = pic1)
# @app.route("/graphs")

@app.route("/")
def index():
    ticker = request.args.get("ticker", "")
    name_, sector, industry, country, employees, volume, market_cap = "", "", "", "", "", "", ""
    ptoe, ptob, dividend, dtoe, price = '', '', '', '', ''
    if ticker:
        _ticker_ = ticker_input(ticker)
        name_ = _ticker_[0]
        sector = _ticker_[2]
        industry = _ticker_[3]
        country = _ticker_[4]
        employees = _ticker_[5]
        volume = _ticker_[6]
        market_cap = _ticker_[7]
        price = _ticker_[8]
        ptoe = _ticker_[9]
        ptob = _ticker_[10]
        dividend = _ticker_[11]
        dtoe = _ticker_[12]
        if employees == -1:
            employees = "Information currently unavailable"
        if ptoe == -1:
            ptoe = "Information currently unavailable"
        if ptob == -1:
            ptob = "Information currently unavailable"
        if dividend == -1:
            dividend = "Information currently unavailable"
        if dtoe == -1:
            dtoe = "Information currently unavailable"
        if name_ == -1 or name_ == "":
            name_ = "Information currently unavailable"
        if sector == -1 or name_ == "":
            sector = "Information currently unavailable"
        if industry == -1 or name_ == "":
            industry = "Information currently unavailable"
        if country == -1 or name_ == "":
            country = "Information currently unavailable"
        if volume == -1 or name_ == "":
            volume = "Information currently unavailable"
        if market_cap == -1 or name_ == "":
            market_cap = "Information currently unavailable"
    else:
        _ticker_ = ""
    #stock = finvizfinance(ticker)
    #stock_fundament = stock.TickerFundament()
    try:
        return (
            """
                <div> Insert your query: </div>
                <form action="" method="get">
                    <input type="text" name="ticker">
                    <input type="submit" value="Search">
                </form>
            """
            + ticker
            + "<p>"
            + "Company: " + str(name_) + "<p>"
            + "Sector: " + str(sector) + "<p>"
            + "Industry: " + str(industry) + "<p>"
            + "Country: " + str(country) + "<p>"
            + "Employees: " + str(employees) + "<p>"
            + "Volume: " + str(volume) + "<p>"
            + "Market capitalization: " + str(market_cap) + "<p>"
            + "Price: " + str(price) + "<p>"
            + "P/E: " + str(ptoe) + "<p>"
            + "P/B: " + str(ptob) + "<p>"
            + "Dividend: " + str(dividend) + "<p>"
            + "D/E: " + str(dtoe) + "<p>"
            + "<p>"
        )
    except ValueError:
        return """
        <div> Invalid input </div>
               """


def ticker_input(tckr):
    # '''A user input procedure with a back-end call.'''
    try:
        try:
            finvizfinance(tckr)
            print("Ticker found!\n")
        except:
            print("Invalid ticker!\n")
            exit()
        check = if_row_exists(tckr)
        if not check:
            update_data(tckr)
        else:
            insert_data(tckr)
            print("Ticker not found! Try another one.")
        # get_data(tckr)
        # print("\n")
        # return ("""<div> fdgdfgh </div>""")
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(tckr)
        stock_fundament = stock.TickerFundament()
        name_ = stock_fundament['Company']
        select_query = """SELECT Company, Ticker, Sector, Industry, Country, 
                          Employees, Volume, Market_Capitalization, Price,
                          PriceToEarnings, PriceToBook, Dividend, DebtToEquity
                          FROM stock_data WHERE Company = %s
                       """
        to_select = (name_,)
        cursor.execute(select_query, to_select)
        data = cursor.fetchone()
        # if data[5] == -1:
        #     data[5] = "Information currently unavailable"
        return data
        #_ptoe, _ptob, _div, _dtoe = -1, -1, -1, -1
        #if type((stock_fundament['P/E'])) != str:
        #    _ptoe = float(stock_fundament['P/E'])
        #if type((stock_fundament['P/B'])) != str:
        #    _ptob = float(stock_fundament['P/B'])
        #if type((stock_fundament['Dividend'])) != str:
        #    _div = float(stock_fundament['Dividend'])
        #if type((stock_fundament['Debt/Eq'])) != str:
        #    _dtoe = float(stock_fundament['Debt/Eq'])
        #return [stock_fundament['Company'], stock_fundament['Sector'],
        #        stock_fundament['Industry'], stock_fundament['Country'],
        #        stock_fundament['Employees'], stock_fundament['Volume'],
        #        stock_fundament['Market Cap'], _ptoe, _ptob, _div, _dtoe]
    except ValueError:
        return "invalid input"


@app.route("/g")
def home():
    data = [
        ("01-01-2020", 1597),
        ("02-01-2020", 1456),
        ("03-01-2020", 1908),
        ("04-01-2020", 896),
        ("05-01-2020", 755),
        ("06-01-2020", 453),
        ("07-01-2020", 1100),
        ("08-01-2020", 1235),
        ("09-01-2020", 1478),
    ]

    _labels = [row[0] for row in data]
    _values = [row[1] for row in data]

    return render_template("graph0.html", labels=_labels, values=_values)

@app.route("/graphs/open")
def chart():
    ticker = request.args.get("ticker", "")
    d0, d1, d2, timeSeries = '', '', '', ''
    _open, _open_keys, high, highKeys, low, lowKeys, close, closeKeys, volume, vKeys = [], [], [], [], [], [], [], [], [], []
    r_open, r_open_keys, rhigh, rhighKeys, rlow, rlowKeys, rclose, rcloseKeys, rvolume, rvKeys = [], [], [], [], [], [], [], [], [], []
    openLabels, openValues, highLabels, highValues = [], [], [], []
    if ticker:
        data = chart_input(ticker)
        d0, d1 = data[0], str(data[1])
        timeSeries = data[2]['Time Series (5min)']
        for five_minutes_list in timeSeries:
            _open.append(timeSeries[five_minutes_list]['1. open'])
            _open_keys.append(str(five_minutes_list))
            high.append(timeSeries[five_minutes_list]['2. high'])
            highKeys.append(str(five_minutes_list))
            low.append(timeSeries[five_minutes_list]['3. low'])
            lowKeys.append(str(five_minutes_list))
            close.append(timeSeries[five_minutes_list]['4. close'])
            closeKeys.append(str(five_minutes_list))
            volume.append(timeSeries[five_minutes_list]['5. volume'])
            vKeys.append(str(five_minutes_list))
        for i in range(-1, -len(_open), -1):
            r_open.append(_open[i])
            r_open_keys.append(_open_keys[i])
        for i in range(-1, -len(high), -1):
            rhigh.append(high[i])
            rhighKeys.append(highKeys[i])
        for i in range(-1, -len(low), -1):
            rlow.append(low[i])
            rlowKeys.append(lowKeys[i])
        for i in range(-1, -len(close), -1):
            rclose.append(close[i])
            rcloseKeys.append(closeKeys[i])
        for i in range(-1, -len(volume), -1):
            rvolume.append(volume[i])
            rvKeys.append(vKeys[i])
        openAll, highAll, lowAll, closeAll, volumeAll = [], [], [], [], []
        for i in range(len(r_open)):
            tuple_ = (r_open_keys[i], r_open[i])
            openAll.append(tuple_)
        for i in range(len(rhigh)):
            tuple_ = (rhighKeys[i], rhigh[i])
            highAll.append(tuple_)
        for i in range(len(rlow)):
            tuple_ = (rlowKeys[i], rlow[i])
            lowAll.append(tuple_)
        for i in range(len(rclose)):
            tuple_ = (rcloseKeys[i], rclose[i])
            closeAll.append(tuple_)
        for i in range(len(rvolume)):
            tuple_ = (rvKeys[i], rvolume[i])
            volumeAll.append(tuple_)
        openLabels = [row[0] for row in openAll]
        openValues = [row[1] for row in openAll]
        highLabels = [row[0] for row in highAll]
        highValues = [row[1] for row in highAll]
        lowLabels = [row[0] for row in lowAll]
        lowValues = [row[1] for row in lowAll]
        closeLabels = [row[0] for row in closeAll]
        closeValues = [row[1] for row in closeAll]
        vLabels = [row[0] for row in volumeAll]
        vValues = [row[1] for row in volumeAll]
    else:
        data = ""
    try:
        return ("""
                    <div> Insert your query: </div>
                    <form action="" method="get">
                        <input type="text" name="ticker">
                        <input type="submit" value="Search">
                    </form>
                """ + ticker + "<p>" + d0 + "<p>" + d1 + "<p>"
                    + render_template("graph1.html", labels=openLabels, values=openValues) + "<p>"
                    # + render_template("graph2.html", labels=highLabels, values=highValues) + "<p>"
                    # + "dsgfjhb"
                    # + render_template("graph2.html", labels=highLabels, values=highValues) + "<p>"
        )
    except ValueError:
        return "invalid operation"    


@app.route("/graphs/open")
def chart_input(tckr):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(tckr)
        stock_fundament = stock.TickerFundament()
        name_ = stock_fundament['Company']
        to_select = (name_,)
        query = """SELECT * from MarketHistory WHERE stock_name = %s"""
        cursor.execute(query, to_select)
        data = cursor.fetchone()
        return data
    except ValueError:
        return ("invalid input")


@app.route("/graphs/high")
def chart_h():
    ticker = request.args.get("ticker", "")
    d0, d1, d2, timeSeries = '', '', '', ''
    _open, _open_keys, high, highKeys, low, lowKeys, close, closeKeys, volume, vKeys = [], [], [], [], [], [], [], [], [], []
    r_open, r_open_keys, rhigh, rhighKeys, rlow, rlowKeys, rclose, rcloseKeys, rvolume, rvKeys = [], [], [], [], [], [], [], [], [], []
    openLabels, openValues, highLabels, highValues = [], [], [], []
    if ticker:
        data = chart_input(ticker)
        d0, d1 = data[0], str(data[1])
        timeSeries = data[2]['Time Series (5min)']
        for five_minutes_list in timeSeries:
            _open.append(timeSeries[five_minutes_list]['1. open'])
            _open_keys.append(str(five_minutes_list))
            high.append(timeSeries[five_minutes_list]['2. high'])
            highKeys.append(str(five_minutes_list))
            low.append(timeSeries[five_minutes_list]['3. low'])
            lowKeys.append(str(five_minutes_list))
            close.append(timeSeries[five_minutes_list]['4. close'])
            closeKeys.append(str(five_minutes_list))
            volume.append(timeSeries[five_minutes_list]['5. volume'])
            vKeys.append(str(five_minutes_list))
        for i in range(-1, -len(_open), -1):
            r_open.append(_open[i])
            r_open_keys.append(_open_keys[i])
        for i in range(-1, -len(high), -1):
            rhigh.append(high[i])
            rhighKeys.append(highKeys[i])
        for i in range(-1, -len(low), -1):
            rlow.append(low[i])
            rlowKeys.append(lowKeys[i])
        for i in range(-1, -len(close), -1):
            rclose.append(close[i])
            rcloseKeys.append(closeKeys[i])
        for i in range(-1, -len(volume), -1):
            rvolume.append(volume[i])
            rvKeys.append(vKeys[i])
        openAll, highAll, lowAll, closeAll, volumeAll = [], [], [], [], []
        for i in range(len(r_open)):
            tuple_ = (r_open_keys[i], r_open[i])
            openAll.append(tuple_)
        for i in range(len(rhigh)):
            tuple_ = (rhighKeys[i], rhigh[i])
            highAll.append(tuple_)
        for i in range(len(rlow)):
            tuple_ = (rlowKeys[i], rlow[i])
            lowAll.append(tuple_)
        for i in range(len(rclose)):
            tuple_ = (rcloseKeys[i], rclose[i])
            closeAll.append(tuple_)
        for i in range(len(rvolume)):
            tuple_ = (rvKeys[i], rvolume[i])
            volumeAll.append(tuple_)
        openLabels = [row[0] for row in openAll]
        openValues = [row[1] for row in openAll]
        highLabels = [row[0] for row in highAll]
        highValues = [row[1] for row in highAll]
        lowLabels = [row[0] for row in lowAll]
        lowValues = [row[1] for row in lowAll]
        closeLabels = [row[0] for row in closeAll]
        closeValues = [row[1] for row in closeAll]
        vLabels = [row[0] for row in volumeAll]
        vValues = [row[1] for row in volumeAll]
    else:
        data = ""
    try:
        return ("""
                    <div> Insert your query: </div>
                    <form action="" method="get">
                        <input type="text" name="ticker">
                        <input type="submit" value="Search">
                    </form>
                """ + ticker + "<p>" + d0 + "<p>" + d1 + "<p>"
                    + render_template("graph2.html", labels=highLabels, values=highValues) + "<p>"
                    # + render_template("graph2.html", labels=highLabels, values=highValues) + "<p>"
                    # + "dsgfjhb"
                    # + render_template("graph2.html", labels=highLabels, values=highValues) + "<p>"
        )
    except ValueError:
        return "invalid operation"    


@app.route("/graphs/high")
def chart_input_h(tckr):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(tckr)
        stock_fundament = stock.TickerFundament()
        name_ = stock_fundament['Company']
        to_select = (name_,)
        query = """SELECT * from MarketHistory WHERE stock_name = %s"""
        cursor.execute(query, to_select)
        data = cursor.fetchone()
        return data
    except ValueError:
        return ("invalid input")


@app.route("/graphs/low")
def chart_l():
    ticker = request.args.get("ticker", "")
    d0, d1, d2, timeSeries = '', '', '', ''
    _open, _open_keys, high, highKeys, low, lowKeys, close, closeKeys, volume, vKeys = [], [], [], [], [], [], [], [], [], []
    r_open, r_open_keys, rhigh, rhighKeys, rlow, rlowKeys, rclose, rcloseKeys, rvolume, rvKeys = [], [], [], [], [], [], [], [], [], []
    openLabels, openValues, highLabels, highValues = [], [], [], []
    if ticker:
        data = chart_input(ticker)
        d0, d1 = data[0], str(data[1])
        timeSeries = data[2]['Time Series (5min)']
        for five_minutes_list in timeSeries:
            _open.append(timeSeries[five_minutes_list]['1. open'])
            _open_keys.append(str(five_minutes_list))
            high.append(timeSeries[five_minutes_list]['2. high'])
            highKeys.append(str(five_minutes_list))
            low.append(timeSeries[five_minutes_list]['3. low'])
            lowKeys.append(str(five_minutes_list))
            close.append(timeSeries[five_minutes_list]['4. close'])
            closeKeys.append(str(five_minutes_list))
            volume.append(timeSeries[five_minutes_list]['5. volume'])
            vKeys.append(str(five_minutes_list))
        for i in range(-1, -len(_open), -1):
            r_open.append(_open[i])
            r_open_keys.append(_open_keys[i])
        for i in range(-1, -len(high), -1):
            rhigh.append(high[i])
            rhighKeys.append(highKeys[i])
        for i in range(-1, -len(low), -1):
            rlow.append(low[i])
            rlowKeys.append(lowKeys[i])
        for i in range(-1, -len(close), -1):
            rclose.append(close[i])
            rcloseKeys.append(closeKeys[i])
        for i in range(-1, -len(volume), -1):
            rvolume.append(volume[i])
            rvKeys.append(vKeys[i])
        openAll, highAll, lowAll, closeAll, volumeAll = [], [], [], [], []
        for i in range(len(r_open)):
            tuple_ = (r_open_keys[i], r_open[i])
            openAll.append(tuple_)
        for i in range(len(rhigh)):
            tuple_ = (rhighKeys[i], rhigh[i])
            highAll.append(tuple_)
        for i in range(len(rlow)):
            tuple_ = (rlowKeys[i], rlow[i])
            lowAll.append(tuple_)
        for i in range(len(rclose)):
            tuple_ = (rcloseKeys[i], rclose[i])
            closeAll.append(tuple_)
        for i in range(len(rvolume)):
            tuple_ = (rvKeys[i], rvolume[i])
            volumeAll.append(tuple_)
        openLabels = [row[0] for row in openAll]
        openValues = [row[1] for row in openAll]
        highLabels = [row[0] for row in highAll]
        highValues = [row[1] for row in highAll]
        lowLabels = [row[0] for row in lowAll]
        lowValues = [row[1] for row in lowAll]
        closeLabels = [row[0] for row in closeAll]
        closeValues = [row[1] for row in closeAll]
        vLabels = [row[0] for row in volumeAll]
        vValues = [row[1] for row in volumeAll]
    else:
        data = ""
    try:
        return ("""
                    <div> Insert your query: </div>
                    <form action="" method="get">
                        <input type="text" name="ticker">
                        <input type="submit" value="Search">
                    </form>
                """ + ticker + "<p>" + d0 + "<p>" + d1 + "<p>"
                    + render_template("graph3.html", labels=lowLabels, values=lowValues) + "<p>"
        )
    except ValueError:
        return "invalid operation"    


@app.route("/graphs/low")
def chart_input_l(tckr):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(tckr)
        stock_fundament = stock.TickerFundament()
        name_ = stock_fundament['Company']
        to_select = (name_,)
        query = """SELECT * from MarketHistory WHERE stock_name = %s"""
        cursor.execute(query, to_select)
        data = cursor.fetchone()
        return data
    except ValueError:
        return ("invalid input")


@app.route("/graphs/close")
def chart_c():
    ticker = request.args.get("ticker", "")
    d0, d1, d2, timeSeries = '', '', '', ''
    _open, _open_keys, high, highKeys, low, lowKeys, close, closeKeys, volume, vKeys = [], [], [], [], [], [], [], [], [], []
    r_open, r_open_keys, rhigh, rhighKeys, rlow, rlowKeys, rclose, rcloseKeys, rvolume, rvKeys = [], [], [], [], [], [], [], [], [], []
    openLabels, openValues, highLabels, highValues = [], [], [], []
    if ticker:
        data = chart_input(ticker)
        d0, d1 = data[0], str(data[1])
        timeSeries = data[2]['Time Series (5min)']
        for five_minutes_list in timeSeries:
            _open.append(timeSeries[five_minutes_list]['1. open'])
            _open_keys.append(str(five_minutes_list))
            high.append(timeSeries[five_minutes_list]['2. high'])
            highKeys.append(str(five_minutes_list))
            low.append(timeSeries[five_minutes_list]['3. low'])
            lowKeys.append(str(five_minutes_list))
            close.append(timeSeries[five_minutes_list]['4. close'])
            closeKeys.append(str(five_minutes_list))
            volume.append(timeSeries[five_minutes_list]['5. volume'])
            vKeys.append(str(five_minutes_list))
        for i in range(-1, -len(_open), -1):
            r_open.append(_open[i])
            r_open_keys.append(_open_keys[i])
        for i in range(-1, -len(high), -1):
            rhigh.append(high[i])
            rhighKeys.append(highKeys[i])
        for i in range(-1, -len(low), -1):
            rlow.append(low[i])
            rlowKeys.append(lowKeys[i])
        for i in range(-1, -len(close), -1):
            rclose.append(close[i])
            rcloseKeys.append(closeKeys[i])
        for i in range(-1, -len(volume), -1):
            rvolume.append(volume[i])
            rvKeys.append(vKeys[i])
        openAll, highAll, lowAll, closeAll, volumeAll = [], [], [], [], []
        for i in range(len(r_open)):
            tuple_ = (r_open_keys[i], r_open[i])
            openAll.append(tuple_)
        for i in range(len(rhigh)):
            tuple_ = (rhighKeys[i], rhigh[i])
            highAll.append(tuple_)
        for i in range(len(rlow)):
            tuple_ = (rlowKeys[i], rlow[i])
            lowAll.append(tuple_)
        for i in range(len(rclose)):
            tuple_ = (rcloseKeys[i], rclose[i])
            closeAll.append(tuple_)
        for i in range(len(rvolume)):
            tuple_ = (rvKeys[i], rvolume[i])
            volumeAll.append(tuple_)
        openLabels = [row[0] for row in openAll]
        openValues = [row[1] for row in openAll]
        highLabels = [row[0] for row in highAll]
        highValues = [row[1] for row in highAll]
        lowLabels = [row[0] for row in lowAll]
        lowValues = [row[1] for row in lowAll]
        closeLabels = [row[0] for row in closeAll]
        closeValues = [row[1] for row in closeAll]
        vLabels = [row[0] for row in volumeAll]
        vValues = [row[1] for row in volumeAll]
    else:
        data = ""
    try:
        return ("""
                    <div> Insert your query: </div>
                    <form action="" method="get">
                        <input type="text" name="ticker">
                        <input type="submit" value="Search">
                    </form>
                """ + ticker + "<p>" + d0 + "<p>" + d1 + "<p>"
                    + render_template("graph4.html", labels=closeLabels, values=closeValues) + "<p>"
        )
    except ValueError:
        return "invalid operation"    


@app.route("/graphs/close")
def chart_input_c(tckr):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(tckr)
        stock_fundament = stock.TickerFundament()
        name_ = stock_fundament['Company']
        to_select = (name_,)
        query = """SELECT * from MarketHistory WHERE stock_name = %s"""
        cursor.execute(query, to_select)
        data = cursor.fetchone()
        return data
    except ValueError:
        return ("invalid input")


@app.route("/graphs/volume")
def chart_v():
    ticker = request.args.get("ticker", "")
    d0, d1, d2, timeSeries = '', '', '', ''
    _open, _open_keys, high, highKeys, low, lowKeys, close, closeKeys, volume, vKeys = [], [], [], [], [], [], [], [], [], []
    r_open, r_open_keys, rhigh, rhighKeys, rlow, rlowKeys, rclose, rcloseKeys, rvolume, rvKeys = [], [], [], [], [], [], [], [], [], []
    openLabels, openValues, highLabels, highValues = [], [], [], []
    if ticker:
        data = chart_input(ticker)
        d0, d1 = data[0], str(data[1])
        timeSeries = data[2]['Time Series (5min)']
        for five_minutes_list in timeSeries:
            _open.append(timeSeries[five_minutes_list]['1. open'])
            _open_keys.append(str(five_minutes_list))
            high.append(timeSeries[five_minutes_list]['2. high'])
            highKeys.append(str(five_minutes_list))
            low.append(timeSeries[five_minutes_list]['3. low'])
            lowKeys.append(str(five_minutes_list))
            close.append(timeSeries[five_minutes_list]['4. close'])
            closeKeys.append(str(five_minutes_list))
            volume.append(timeSeries[five_minutes_list]['5. volume'])
            vKeys.append(str(five_minutes_list))
        for i in range(-1, -len(_open), -1):
            r_open.append(_open[i])
            r_open_keys.append(_open_keys[i])
        for i in range(-1, -len(high), -1):
            rhigh.append(high[i])
            rhighKeys.append(highKeys[i])
        for i in range(-1, -len(low), -1):
            rlow.append(low[i])
            rlowKeys.append(lowKeys[i])
        for i in range(-1, -len(close), -1):
            rclose.append(close[i])
            rcloseKeys.append(closeKeys[i])
        for i in range(-1, -len(volume), -1):
            rvolume.append(volume[i])
            rvKeys.append(vKeys[i])
        openAll, highAll, lowAll, closeAll, volumeAll = [], [], [], [], []
        for i in range(len(r_open)):
            tuple_ = (r_open_keys[i], r_open[i])
            openAll.append(tuple_)
        for i in range(len(rhigh)):
            tuple_ = (rhighKeys[i], rhigh[i])
            highAll.append(tuple_)
        for i in range(len(rlow)):
            tuple_ = (rlowKeys[i], rlow[i])
            lowAll.append(tuple_)
        for i in range(len(rclose)):
            tuple_ = (rcloseKeys[i], rclose[i])
            closeAll.append(tuple_)
        for i in range(len(rvolume)):
            tuple_ = (rvKeys[i], rvolume[i])
            volumeAll.append(tuple_)
        openLabels = [row[0] for row in openAll]
        openValues = [row[1] for row in openAll]
        highLabels = [row[0] for row in highAll]
        highValues = [row[1] for row in highAll]
        lowLabels = [row[0] for row in lowAll]
        lowValues = [row[1] for row in lowAll]
        closeLabels = [row[0] for row in closeAll]
        closeValues = [row[1] for row in closeAll]
        vLabels = [row[0] for row in volumeAll]
        vValues = [row[1] for row in volumeAll]
    else:
        data = ""
    try:
        return ("""
                    <div> Insert your query: </div>
                    <form action="" method="get">
                        <input type="text" name="ticker">
                        <input type="submit" value="Search">
                    </form>
                """ + ticker + "<p>" + d0 + "<p>" + d1 + "<p>"
                    + render_template("graph5.html", labels=vLabels, values=vValues) + "<p>"
        )
    except ValueError:
        return "invalid operation"    


@app.route("/graphs/volume")
def chart_input_v(tckr):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        stock = finvizfinance(tckr)
        stock_fundament = stock.TickerFundament()
        name_ = stock_fundament['Company']
        to_select = (name_,)
        query = """SELECT * from MarketHistory WHERE stock_name = %s"""
        cursor.execute(query, to_select)
        data = cursor.fetchone()
        return data
    except ValueError:
        return ("invalid input")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)

# if __name__ == "__main__":
#    app.run(host="127.0.0.1", port=3001, debug=True)
# a
