# A programme that adds to the already configured FinAssistant database the table that
# is going to contain the stock market data.

import psycopg2 as pz

try:
    connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
    cursor = connection.cursor()
    # The PostgreSQL script which creates a new table.
    new_table = """CREATE TABLE StockMarket (
                    name VARCHAR ( 100 ) PRIMARY KEY,
                    priceToEarnings DOUBLE PRECISION,
                    priceToBook DOUBLE PRECISION,
                    forwardPE DOUBLE PRECISION,
                    marketCapitalization VARCHAR ( 200 ) NOT NULL,
                    earnPerShare_ttm DOUBLE PRECISION,
                    earnPerShare_nextYear VARCHAR ( 200 ) NOT NULL,
                    dividend DOUBLE PRECISION,
                    debtToEquity DOUBLE PRECISION,
                    high52wks VARCHAR ( 200 ) NOT NULL
                )"""
    cursor.execute(new_table)
    connection.commit()
    print("The table containing the firms' stock market data has been successfully created in the Heroku "
          "PostgreSQL database.")

except (Exception, pz.Error) as error:
    print("Connection terminated because of", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("The PostgreSQL connection to the Heroku database has been closed.")
