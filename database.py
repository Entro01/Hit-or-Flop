# download the credits.csv at 'model-files/datasets/credits.csv' from the dataset archive linked in 'model-files\datasets\datasets link.txt'.
# execute this file to populate your database.

import pandas as pd
from sqlalchemy import create_engine
from mysql.connector import connect
from tqdm import tqdm

connection = connect(
    host='localhost',
    user='Entro01',
    password='password',
    database='store',
    auth_plugin='mysql_native_password'
 )


if connection.is_connected():
     db_info = connection.get_server_info()
     print("Connected to MySQL Server version ", db_info)
     connection.close()
     print("MySQL connection is closed")
else:
    print("Error while connecting to MySQL")

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
       chunk.to_sql('credits', engine, if_exists='append', index=False)
       # Update the progress bar
       pbar.update(len(chunk))