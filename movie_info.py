from mysql.connector import connect, Error

def connect_to_db():
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
           return connection
   except Error as e:
       print("Error while connecting to MySQL", e)
       return None
   
def get_credits(connection, actor, director):
    cursor = connection.cursor(buffered=True)
   
    # Get actor's profession and known titles
    cursor.execute(f"SELECT primaryProfession, knownForTitles FROM credits WHERE primaryName = '{actor}'")
    professionA, titlesA = cursor.fetchone()
    cursor.fetchall() # Fetch and discard remaining rows
   
    # Get director's profession and known titles
    cursor.execute(f"SELECT primaryProfession, knownForTitles FROM credits WHERE primaryName = '{director}'")
    professionD, titlesD = cursor.fetchone()
    cursor.fetchall() # Fetch and discard remaining rows
   
    # Close the cursor
    cursor.close()
   
    return professionA, titlesA, professionD, titlesD

def generate_sentence(actor, director, result, probabilities, professionA, titlesA, professionD, titlesD):
  # Split the professions and titles into lists
  professionsA = professionA.split(',')
  titlesA = titlesA.replace('[','').replace(']','')
  titlesA = titlesA.replace('\'','').replace('\'','')
  professionsD = professionD.split(',')
  titlesD = titlesD.replace('[','').replace(']','')
  titlesD = titlesD.replace('\'','').replace('\'','')

  # Join the professions and titles with commas and spaces
  professionsA = ', '.join(professionsA)
  professionsD = ', '.join(professionsD)

  sentence = f"The upcoming {actor} and {director} movie is predicted to have a {probabilities}% chance of being a {result}. {actor}'s past credits as {professionsA} include: {titlesA} and {director}'s past credits as {professionsD} include: {titlesD}. Using the provided context, an explanation for their predicted success rate is that"
  return sentence

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

def generate_paragraph(sentence):
   tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
   model = GPT2LMHeadModel.from_pretrained('gpt2')
   encoded_input = tokenizer(sentence, return_tensors='pt')
   output = model.generate(**encoded_input, max_length=400, do_sample=True, top_k=50)
   generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
   return generated_text

def generate_movie_prediction(actor, director, result, probabilities):
   # Connect to the database
   connection = connect_to_db()
   
   # Retrieve actor and director credits
   professionA, titlesA, professionD, titlesD = get_credits(connection, actor, director)
   
   # Generate the sentence
   sentence = generate_sentence(actor, director, result, probabilities, professionA, titlesA, professionD, titlesD)
   
   # Generate the paragraph
   paragraph = generate_paragraph(sentence)
   
   # Return the paragraph
   return paragraph