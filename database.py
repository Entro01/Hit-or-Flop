import pandas as pd
from sqlalchemy import create_engine
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

df1 = pd.read_csv('model-files\movie_data.tsv', sep='\t', dtype={4: str})
df2 = pd.read_csv('model-files\work_data.tsv', sep='\t', dtype={4: str})

df1 = df1.drop(['originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes'], axis=1)
df2 = df2.drop(['birthYear', 'deathYear'], axis=1)

engine = create_engine('mysql+mysqlconnector://Entro01:password@localhost/store')
df1.to_sql('table1', engine, if_exists='replace', index=False)
df2.to_sql('table2', engine, if_exists='replace', index=False)