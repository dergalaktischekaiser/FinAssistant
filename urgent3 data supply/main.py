import psycopg2 as pz
from finvizfinance.quote import finvizfinance
from finviz.screener import Screener
from datetime import datetime, timezone, timedelta


def check_if_row_exists(stockFundament):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # A SELECT PostrgeSQL query which checks whether a row exists or not.
        # stock = finvizfinance(ticker)
        # stock_fundament = stock.TickerFundament()
        cursor.execute("SELECT Company FROM stock_data WHERE Company = %s", (stockFundament['Company'],))
        connection.commit()
        return cursor.fetchone() is None

    except(Exception, pz.Error) as error:
        print("Connection failed:", error)


def insert_timestamp(stockFundament):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        # stock = finvizfinance(ticker)
        # outer_ratings_df = stock.TickerOuterRatings()
        # print((outer_ratings_df))
        # print(Screener())
        # stock_fundament = stock.TickerFundament()
        price = stockFundament['Price']
        name = stockFundament['Company']
        d = datetime.today() - timedelta(days=1)

        insert_query = """INSERT INTO Stock_To_Chart_Data (stock_name, price, time) VALUES (%s, %s, %s)"""
        to_insert = (name, price, d)
        cursor.execute(insert_query, to_insert)
        connection.commit()

    except(Exception, pz.Error) as error:
        print("Connection failed:", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection to stock data closed.\n")


def update_timestamp(stockFundament):
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        price = stockFundament['Price']
        name = stockFundament['Company']
        d = datetime.today() - timedelta(days=1)
        query = """Update Stock_To_Chart_Data set price = %s where stock_name = %s;
                   Update Stock_To_Chart_Data set time = %s where stock_name = %s;"""
        to_update = (price, name, d, name,)
        cursor.execute(query, to_update)
        connection.commit()

    except(Exception, pz.Error) as err:
        print("Connection failed due to:", err)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection closed.")


print("Insert your query:", end=" ")
tckr = input()
print("...preparing to display...\n")
try:
    stock = finvizfinance(tckr)
    print("Ticker found!\n")

except:
    print("Invalid ticker!\n")
    exit()

# stock = finvizfinance(tckr)
stock_fundament = stock.TickerFundament()
check = check_if_row_exists(stock_fundament)
if not check:
    update_timestamp(stock_fundament)
else:
    insert_timestamp(stock_fundament)
