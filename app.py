from flask import Flask, render_template, request, redirect, url_for
from movie_prediction import predict_probabilities

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/')
def root():
  return redirect(url_for('home'))

@app.route('/go_to_prediction')
def go_to_prediction():
  # Get input from the Flask app
  actor = request.args.get('actor', '')
  director = request.args.get('director', '')
  genre = request.args.get('genre', '')

  # Redirect to the prediction page
  return redirect(url_for('predict', actor=actor, director=director, genre=genre))

@app.route('/prediction')
def predict():
  # Get input from the Flask app
  actor = request.args.get('actor', '')
  director = request.args.get('director', '')
  genre = request.args.get('genre', '')

  # Predict probabilities
  probabilities = predict_probabilities(actor, director, genre)

  # Evaluate probabilities
  if probabilities[0][1] > probabilities[0][0]:
    result = 'Hit'
    probability = probabilities[0][1] * 100
  else:
    result = 'Flop'
    probability = probabilities[0][0] * 100

  # Render the appropriate HTML file
  return render_template('prediction.html', result=result, probability=probability)

if __name__ == "__main__":
    app.run(debug=True)