import pandas as pd
from sqlalchemy import create_engine
from mysql.connector import connect, Error
from tqdm import tqdm

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

# Create a SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://Entro01:password@localhost/store')

# Define the chunk size
chunk_size = 10000 # Adjust this value depending on your available memory

# Get the total number of rows in the CSV file
total_rows = sum(1 for _ in open('model-files/datasets/credits.csv', 'r', encoding='utf-8')) - 1 # minus the header

# Initialize a progress bar
with tqdm(total=total_rows, unit='rows') as pbar:
   # Loop over the chunks of the DataFrame
   for chunk in pd.read_csv('model-files/datasets/credits.csv', chunksize=chunk_size):
       # Insert the chunk into the database
       chunk.to_sql('test', engine, if_exists='append', index=False)
       # Update the progress bar
       pbar.update(len(chunk))