import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

# Load the dataset
df = pd.read_csv('dataset.csv')

# Encode the categorical values
le = LabelEncoder()
df['actor'] = le.fit_transform(df['actor'])
mapping_actor = dict(zip(le.classes_, range(len(le.classes_))))
df['director'] = le.fit_transform(df['director'])
mapping_director = dict(zip(le.classes_, range(len(le.classes_))))
df['genre'] = le.fit_transform(df['genre'])
mapping_genre = dict(zip(le.classes_, range(len(le.classes_))))

# Convert the continuous label into a binary label
df['label'] = df['label'].apply(lambda x: 1 if x >= 0.5 else 0)

# Train the model
X = df.drop(columns = ['label'])
y = df['label']

model = LogisticRegression(max_iter = 1000)
model.fit(X, y)

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
