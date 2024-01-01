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

from transformers import pipeline

# Initialize the generator
generator = pipeline('text-generation', model='mistralai/Mixtral-8x7B-Instruct-v0.1')

# Define your inputs
inputs = f"The cast includes Chris Pratt, directed by Steven Spielberg. If they were to release a movie together today, it would most likely be a hit. Write a short paragraph explaining why by mentioning their past works."

# Generate text
output = generator(inputs, max_length=1000)[0]['generated_text']

print(output)
