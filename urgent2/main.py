import psycopg2 as pz


def create_favourite_stocks_table():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        favourite_stocks_table_creation_query = """CREATE TABLE IF NOT EXISTS User_To_Favourite_Stocks (
                                                    user_id BIGINT REFERENCES Users(id),
                                                    stock_name TEXT REFERENCES stock_data(Company),
                                                    initial_price REAL
                                                )"""
        cursor.execute(favourite_stocks_table_creation_query)
        connection.commit()

    except(Exception, pz.Error) as error:
        print("Connection failed due to", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection closed!\n")


def add_column_added_at():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        add_column_query = """ALTER TABLE User_To_Favourite_Stocks ADD COLUMN added_at TIMESTAMP"""
        cursor.execute(add_column_query)
        connection.commit()
        print("A column has been added!")

    except(Exception, pz.Error) as err:
        print("A column has not been added:", err)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection closed.")


# create_favourite_stocks_table()
# add_column_added_at()
"""
try:
    conn = pz.connect(user='yhxvtdvlnvmtxs',
                            password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                            host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                            port='5432',
                            database='d5fre91hfg8vvf')
    cur = conn.cursor()
    query = """ """ALTER TABLE User_To_Favourite_Stocks DROP COLUMN added_at""""""
    cur.execute(query)
    conn.commit()
    print("deleted")
    query1 = """"""ALTER TABLE
                User_To_Favourite_Stocks ADD COLUMN added_at timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP""""""
    cur.execute(query1)
    conn.commit()
    print("created")

except(Exception, pz.Error) as err:
    print(err)

finally:
    if (conn):
        cur.close()
        conn.close()
        print("Connection closed")"""


def print_table():
    try:
        conn_ = pz.connect(user='yhxvtdvlnvmtxs',
                          password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                          host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                          port='5432',
                          database='d5fre91hfg8vvf')
        cur = conn_.cursor()
        select_all_query = """SELECT * FROM stock_data"""
        cur.execute(select_all_query)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except(Exception, pz.Error) as err:
        print(err)
    finally:
        if(conn_):
            cur.close()
            conn_.close()
            print("Connection closed")


print_table()
