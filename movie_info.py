from mysql.connector import connect, Error

try:
    connection = connect(
        host='localhost',
        user='Entro01',
        password='password',
        database='store'
    )
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")

