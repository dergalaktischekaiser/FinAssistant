from finvizfinance.quote import finvizfinance
# from finviz.screener import Screener
import psycopg2 as pz
from datetime import datetime
import time


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
        if (connection):
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
            for row in rows:
                dt = datetime.utcnow()
                if dt.hour >= 23:
                    break
                ticker = row[1]
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
                to_update = (name, name,
                             ticker, name,
                             sector, name,
                             industry, name,
                             country, name,
                             employees, name,
                             volume, name,
                             marketcap, name,
                             price, name,
                             ptoe, name,
                             ptob, name,
                             dividend, name,
                             dtoe, name,)
                upd_query = """Update stock_data set Company = %s where Company = %s;
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
                cursor.execute(upd_query, to_update)
                connection.commit()
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


# def update(tckr):
automatic_update()
