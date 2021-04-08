# A script creating the general database hosting on my pgAdmin.

import psycopg2 as pz

connection = pz.connect(database="postgres",
                        user='postgres',
                        password='ichbindersenat',
                        host='127.0.0.1',
                        port='5432')
connection.autocommit = True
cursor = connection.cursor()

# A PostgreSQL script to create a new database.
creation_query = '''CREATE database FinAssistant'''
cursor.execute(creation_query)
print("Database FinAssistant has been successfully created.")
connection.close()
