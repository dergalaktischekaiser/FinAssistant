import psycopg2 as pz


def delete_rows():
    try:
        connection = pz.connect(user='yhxvtdvlnvmtxs',
                                password='bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda',
                                host='ec2-54-216-155-253.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='d5fre91hfg8vvf')
        print("Procedure begun...")
        amount = 0
        cursor = connection.cursor()
        select_all = """SELECT * from stock_data"""
        cursor.execute(select_all)
        rows = cursor.fetchall()
        for row in rows:
            # print(row)
            name = row[0]
            q0 = """SELECT PriceToEarnings FROM stock_data WHERE Company = %s;"""
            q1 = """SELECT Market_Capitalization FROM stock_data WHERE Company = %s;"""
            q2 = """SELECT Employees FROM stock_data WHERE Company = %s;"""
            cursor.execute(q0, (name,))
            ptoe = cursor.fetchone()
            # print(*num, end=" ")
            cursor.execute(q1, (name,))
            marketCap = cursor.fetchone()
            # print(*num, end=" ")
            cursor.execute(q2, (name,))
            empl = cursor.fetchone()
            # print(ptoe, marketCap, empl)
            if ptoe[0] == -1.0 and marketCap[0] == '-' and empl[0] == -1:
                delete_query = """DELETE FROM stock_data WHERE Company = %s;"""
                cursor.execute(delete_query, (name,))
                connection.commit()
                ++amount
                print("Information about", name, "deleted.")
            # print(*num, end=" ")
        print(amount, "odd rows deleted.")

    except(Exception, pz.Error) as error:
        print("Couldn't delete due to", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Deleted.")


if __name__ == "__main__":
    delete_rows()
