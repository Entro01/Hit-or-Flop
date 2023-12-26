from flask import Flask, render_template
from flask import Flask, request
from movie_prediction import predict_probabilities

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/prediction')
def predict():
   # Get input from the Flask app
   #actor = request.json['actor']
   actor = "Chris Pratt"
   #director = request.json['director']
   director = "Colin Trevorrow"
   #genre = request.json['genre']
   genre = "Action"

   # Predict probabilities
   probabilities = predict_probabilities(actor, director, genre)

   # Evaluate probabilities
   if probabilities[0][0] > probabilities[0][1]:
    result = 'Hit'
    probability = probabilities[0][0] * 100
   else:
    result = 'Flop'
    probability = probabilities[0][1] * 100

   # Render the appropriate HTML file
   return render_template('prediction.html', result=result, probability=probability)

if __name__ == "__main__":
    app.run(debug=True)