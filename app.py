from flask import Flask, render_template, request, redirect, url_for, session
from movie_prediction import predict_probabilities
from movie_info import generate_movie_prediction

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/')
def root():
  return render_template("landing.html")

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
    probability = int(probabilities[0][1] * 100)
  else:
    result = 'Flop'
    probability = int(probabilities[0][0] * 100)

  # Store variables in the session
  session['actor'] = actor
  session['director'] = director
  session['result'] = result
  session['probability'] = probability

  # Render the appropriate HTML file
  return render_template('prediction.html', result=result, probability=probability)

@app.route('/info')
def info():
  actor = session.get('actor', '')
  director = session.get('director', '')
  result = session.get('result', '')
  probability = session.get('probability', '')
  para = generate_movie_prediction(actor, director, result, probability)

  return render_template('info.html', para=para)

if __name__ == "__main__":
    app.run(debug=True)