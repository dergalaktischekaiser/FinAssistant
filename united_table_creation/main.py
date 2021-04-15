# A programme that creates a table containing stock market data to the already configured Heroku PostgreSQL database.
import psycopg2 as pz

# USE THIS SCRIPT TO CREATE THE MAIN POSTGRESQL TABLE IN THE DATABASE


try:
    connection = pz.connect(user='yhxvtdvlnvmtxs',
                            password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                            host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                            port='5432',
                            database='d5fre91hfg8vvf')
    cursor = connection.cursor()
    # The PostgreSQL script which creates a new table.
    new_table = """CREATE TABLE stock_data (
                    Company VARCHAR ( 200 ) PRIMARY KEY,
                    Ticker VARCHAR ( 50 ) NOT NULL,
                    Sector VARCHAR ( 200 ) NOT NULL,
                    Industry VARCHAR ( 200 ) NOT NULL,
                    Country VARCHAR ( 200 ) NOT NULL,
                    Employees INT NOT NULL,
                    Volume VARCHAR ( 200 ) NOT NULL,
                    Market_Capitalization VARCHAR ( 200 ) NOT NULL,
                    Price DOUBLE PRECISION,
                    PriceToEarnings DOUBLE PRECISION,
                    PriceToBook DOUBLE PRECISION,
                    Dividend DOUBLE PRECISION,
                    DebtToEquity DOUBLE PRECISION
                )"""
    cursor.execute(new_table)
    connection.commit()
    print("Table creation successful!\n")

except (Exception, pz.Error) as err:
    print("Connection terminated because of", err)

finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Connection closed.\n")
