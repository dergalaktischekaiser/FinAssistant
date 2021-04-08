# A programme that creates a firm's general information table to the already configured Heroku PostgreSQL database.

import psycopg2 as pz

try:
    connection = pz.connect(user='yhxvtdvlnvmtxs',
                            password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                            host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                            port='5432',
                            database='d5fre91hfg8vvf')
    cursor = connection.cursor()
    # The PostgreSQL script which creates a new table.
    new_table = """CREATE TABLE general_information (
                    corp_name VARCHAR ( 100 ) PRIMARY KEY,
                    sector VARCHAR ( 100 ) NOT NULL,
                    industry VARCHAR ( 100 ) NOT NULL,
                    country VARCHAR ( 100 ) NOT NULL,
                    employees INT NOT NULL,
                    volume VARCHAR ( 200 ) NOT NULL,
                    averageVolume VARCHAR ( 200 ) NOT NULL
                )"""
    cursor.execute(new_table)
    connection.commit()
    print("The general information table has been successfully created in Heroku PostgreSQL database.")

except (Exception, pz.Error) as error:
    print("Connection terminated because of", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("The PostgreSQL connection to the Heroku database has been closed.")
