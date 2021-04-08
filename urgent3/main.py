import psycopg2 as pz


def create_stock_to_chart_table():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        create_stock_to_chart_table_query = """CREATE TABLE IF NOT EXISTS Stock_To_Chart_Data (
                                                stock_name TEXT REFERENCES stock_data(Company),
                                                price REAL,
                                                time TIMESTAMP
                                            )"""
        cursor.execute(create_stock_to_chart_table_query)
        connection.commit()

    except(Exception, pz.Error) as err:
        print("Connection failed due to", err)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection closed!\n")


create_stock_to_chart_table()
