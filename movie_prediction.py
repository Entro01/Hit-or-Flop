from sklearn.ensemble import RandomForestClassifier
import pickle as pk

model = pk.load(open('model-files/model.pkl', 'rb'))

mapping_actor, mapping_director, mapping_genre = pk.load(open('model-files/dicts.pkl', 'rb'))

# Function to predict probabilities
def predict_probabilities(actor, director, genre):
   # Convert input into their respective encodings
   actor_encoded = mapping_actor[actor]
   director_encoded = mapping_director[director]
   genre_encoded = mapping_genre[genre]

   print(actor_encoded)

   # Create a list of encoded features
   encoded_features = [actor_encoded, director_encoded, genre_encoded]

   # Feed the encoded features into the model and output the probabilities
   probabilities = model.predict_proba([encoded_features])

   return probabilities