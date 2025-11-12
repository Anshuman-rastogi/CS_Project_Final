import mysql.connector as msql

def connect_db():
    try:
        cn = msql.connect(
            host='localhost',
            user='root',
            passwd='tuffy',
            database='autocare'
        )
        return cn
    except msql.Error as err:
        print("Database Connection Error:", err)
        return None