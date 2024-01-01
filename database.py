# extract the credits.rar file before running this code

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

# Load the pickled DataFrame
df = pd.read_pickle('model-files\credits.pkl')

# Convert the lists in the 'knownForTitles' column into a format that can be stored in the MySQL database
df['knownForTitles'] = df['knownForTitles'].apply(lambda x: ', '.join(str(item) for item in x))

# Save the DataFrame as an HDF file
df.to_hdf('credits.hdf', key='df')

# Load the DataFrame from the HDF file
df = pd.read_hdf('credits.hdf', 'df')

# Create a SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://Entro01:password@localhost/store')

# Insert the DataFrame into the database
df.to_sql('credits', engine, if_exists='append', index=False)