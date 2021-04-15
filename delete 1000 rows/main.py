import psycopg2 as pz

try:
    connection = pz.connect(user='yhxvtdvlnvmtxs',
                                    password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                    host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                    port='5432',
                                    database='d5fre91hfg8vvf')
    cursor = connection.cursor()
    query = """SELECT * FROM stock_data"""
    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows[6969])
    #for row in rows:
        #print(type(row))
    # print(len(rows))

except(Exception, pz.Error) as err:
    print("Removing failed due to", err)

finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Connection closed!")
