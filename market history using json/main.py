from finvizfinance.quote import finvizfinance
# from finviz.screener import Screener
import psycopg2 as pz
from datetime import datetime, timezone, timedelta
import time
import json
import requests
import alpha_vantage


def createCompactMarketHistoryTable():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # Market History table with 5 min interval
        creation_query = """CREATE TABLE MarketHistory (
                            stock_name TEXT REFERENCES stock_data(Company) PRIMARY KEY,
                            time TIMESTAMP,
                            history JSON NOT NULL
                         )"""
        cursor.execute(creation_query)
        connection.commit()

    except(Exception, pz.Error) as err:
        print("Creation failed because of", err)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Created successfully.")


def drop():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        drop_ = """DROP TABLE MarketHistory"""
        # name_ = "Compact_Market_History_5min"
        cursor.execute(drop_)
        connection.commit()
        print("deleted")

    except(Exception, pz.Error) as err:
        print("failed because of", err)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Deleted successfully.")


def insertJSON_history():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        now = datetime.now()
        ticker = "AMZN"
        tckr = finvizfinance(ticker)
        t = tckr.TickerFundament()['Company']
        # print(t)
        link = "https://www.alphavantage.co/query"
        key = "79861QC266FXQM3C"
        link_parameters = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": ticker,
            "interval": "5min",
            "outputsize": "full",
            "apikey": key
        }
        response = requests.get(link, params=link_parameters)
        dict_ = response.json()
        json_object_for_ticker = json.dumps(dict_)
        # print()
        # print(json_object_for_ticker)
        # print()
        insert = """INSERT INTO MarketHistory (stock_name, time, history)
                 VALUES (%s, %s, %s)"""
        data = (t, now, json_object_for_ticker)
        cursor.execute(insert, data)
        connection.commit()
        print("Inserted.")

    except(Exception, pz.Error) as err:
        print("Couldn't insert because of", err)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Inserted successfully.")


def iterate():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM MarketHistory"""
        cursor.execute(query)
        rows = cursor.fetchall()
        # for row in rows:
        #    print(row)
        #    print()
        #    print()
        #    print()
        print("There are", len(rows), "rows in the MarketHistory database")
        print(len(rows))
    except(Exception, pz.Error) as err:
        print(err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    # createCompactMarketHistoryTable()
    # insertJSON_history()
    iterate()
    # drop()
