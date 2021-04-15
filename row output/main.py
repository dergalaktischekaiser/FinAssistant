from finvizfinance.quote import finvizfinance
from finviz.screener import Screener
import psycopg2 as pz

# A PROGRAMME TO OUTPUT THE POSTGRESQL TABLES TO ENSURE THAT EVERYTHING IS SAVED AS REQUIRED.


def print_rows_of_stock_data():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * from stock_data;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print(len(rows))

    except(Exception, pz.Error) as err:
        print("Failed because of", err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Output finished.")


def print_rows_of_Users():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM Users"""
        cursor.execute(query)
        rows_Users = cursor.fetchall()
        for row in rows_Users:
            print(row)

    except(Exception, pz.Error) as err:
        print("Failed due to", err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Output finished.")


def print_rows_of_User_To_Favourite_Stocks():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM User_To_Favourite_Stocks"""
        cursor.execute(query)
        rows_Users = cursor.fetchall()
        for row in rows_Users:
            print(row)

    except(Exception, pz.Error) as err:
        print("Failed due to", err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Output finished.")


def print_rows_of_Stock_To_Chart_Data():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM Stock_To_Chart_Data"""
        cursor.execute(query)
        rows_Users = cursor.fetchall()
        for row in rows_Users:
            print(row)

    except(Exception, pz.Error) as err:
        print("Failed due to", err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Output finished.")


def print_rows_Stock_To_Chart_Data_15min():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM Stock_To_Chart_Data_15min"""
        cursor.execute(query)
        rows_Users = cursor.fetchall()
        for row in rows_Users:
            print(row)

    except(Exception, pz.Error) as err:
        print("Failed due to", err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Output finished.")


def print_rows_Stock_To_Chart_Data_5min():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        query = """SELECT * FROM Stock_To_Chart_Data_5min"""
        cursor.execute(query)
        rows_Users = cursor.fetchall()
        for row in rows_Users:
            print(row)

    except(Exception, pz.Error) as err:
        print("Failed due to", err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Output finished.")


# print_rows_Stock_To_Chart_Data_5min()
print_rows_of_stock_data()
# print_rows_of_Users()
# print_rows_of_User_To_Favourite_Stocks()
# print_rows_of_Stock_To_Chart_Data()
# print_rows_Stock_To_Chart_Data_15min()
