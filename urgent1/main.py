import psycopg2 as pz


def create_table_of_users():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        create_table_of_users_query = """CREATE TABLE IF NOT EXISTS Users (
                                          id BIGSERIAL PRIMARY KEY,
                                          refresh_token TEXT,
                                          name text,
                                          apple_id text
                                      )"""
        cursor.execute(create_table_of_users_query)
        connection.commit()
        print("The table of users created!\n")

    except(Exception, pz.Error) as err:
        print("Connection failed due to", err)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection closed!\n")


def insert_user_default():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        cursor = connection.cursor()
        insert_query = """INSERT INTO Users (refresh_token, name, apple_id) VALUES (%s, %s, %s)"""
        insert_data = ("", "", "")
        cursor.execute(insert_query, insert_data)
        connection.commit()
        print("A user has been added to the database.", sep="")

    except(Exception, pz.Error) as err:
        print("Connection failed due to", err)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Connection closed.")


# create_table_of_users()
insert_user_default()
