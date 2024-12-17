import os
import joblib
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'vasu@123'  # Change this to a random secret key

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Create the database and the User table
with app.app_context():
    db.create_all()

# Model path

model_path = 'blood_donation_model.pkl'

# Load your model
try:
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Handle the error accordingly

@app.route('/')
def home():
    return redirect(url_for('index'))  # Redirect to index

@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists in the database
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username  # Store the username in session
            return redirect(url_for('index'))
        else:
            return "Invalid username or password", 401  # Return an error for invalid login

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return "Username already exists", 400  # Handle existing user

        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the session
    return redirect(url_for('home'))
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if model is None:
            return "Model not loaded", 500  # Return an error if the model is not loaded

        # Get form data and ensure they are valid
        try:
            months_since_last_donation = float(request.form['months_since_last_donation'])
            months_since_first_donation = float(request.form['months_since_first_donation'])
            number_of_donations = float(request.form['number_of_donations'])

            # Make a prediction
            prediction = model.predict([[months_since_last_donation, months_since_first_donation, number_of_donations]])

            # Render the prediction result
            return render_template('prediction_result.html', prediction=prediction[0])

        except Exception as e:
            return f"Error in prediction: {e}", 400  # Handle prediction errors

    return render_template('prediction.html')

@app.route('/community-impact')

def community_impact():
    return render_template('community_impact.html')


@app.route('/user_friendly')
def user_friendly():
    return render_template('User-Friendly.html')



@app.route('/Predictive_Analytics')
def Predictive_Analytics():
    return render_template('Predictive_Analytics.html')

import pandas as pd
@app.route('/graph')
def graph():
    # Read metrics from CSV
    metrics_df = pd.read_csv('regression_metrics.csv')
    metrics = metrics_df.to_dict(orient='records')  # Convert to list of dictionaries for easy usage in HTML

    return render_template('graph.html', metrics=metrics)


@app.route('/routes')
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule.endpoint}:\t{rule.rule}")
    return "<br>".join(output)


if __name__ == '__main__':
    app.run(debug=True)
