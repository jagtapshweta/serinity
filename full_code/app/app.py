from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import joblib
import re
import pandas as pd
from bson import ObjectId
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Flask App Setup
app = Flask(__name__)
CORS(app)
app.secret_key = "Serenity"  # Secret key for sessions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if user is not authenticated

# MongoDB Setup
client = MongoClient('mongodb+srv://jagtapshweta26:tJy5x6QpWUPt7lEX@serenity.r68xx.mongodb.net/')
db = client['Serenity']
questions_collection = db['Questions']
users_collection = db['Users']
users_response = db['Responses']

# Load Stress Model
stress_model = joblib.load('../model_stress.pkl')

# User Class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user['_id']), user['email'], user['name'])  # Ensure 'name' is present
    return None

@app.route('/chat-bot.html/questions', methods=['GET'])
def get_questions():
    questions = list(questions_collection.find({}, {'_id': 0}))  # Retrieve without MongoDB ObjectID
    return jsonify(questions)

# Home route
@app.route('/')
def index():
    if current_user.is_authenticated:
        userName = current_user.name
        isLogged = True
    else:
        userName = ""
        isLogged = False
    return render_template('index.html', userName=userName, isLogged=isLogged)

# Login Route
@app.route('/login', methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]

    existing_user = users_collection.find_one({"email": email})
    if existing_user and bcrypt.checkpw(password.encode('utf-8'), existing_user["password"]):
        user = User(str(existing_user['_id']), existing_user['email'], existing_user['name'])
        login_user(user)
        return redirect(url_for("index"))
    else:
        flash("Incorrect email or password. Please try again.", "error")
        return render_template('index.html')

# Sign Up Route
@app.route('/create-account', methods=['POST'])
def sign_up():
    userName = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Input validation
    if not userName or not email or not password:
        flash("All fields are required!", "error")
        return render_template('index.html')

    if not validate_email(email):
        flash("Invalid email format!", "error")
        return render_template('index.html')

    # Check if the user already exists
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        flash("Email already registered. Please login instead.", "error")
        return render_template('index.html')

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert new user into the database
    try:
        new_user_id = users_collection.insert_one({
            "name": userName,
            "email": email,
            "password": hashed_password
        }).inserted_id

        # Automatically log in the user after registration
        user = User(str(new_user_id), email, userName)
        login_user(user)
        flash("Account created successfully!", "success")
        return redirect(url_for("index"))
    except Exception as e:
        flash("An error occurred while creating your account. Please try again.", "error")
        return render_template('index.html')

# Logout Route
@app.route('/log-out', methods=['POST'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("index"))

# Chatbot Route
@app.route('/chat-bot.html')
@login_required
def chat_bot():
    return render_template('chat-bot.html')

# Prediction Route
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    responses = data['responses']

    features = pd.DataFrame([{
        'mental_health_history': responses[0],
        'sleep_quality': responses[1],
        'breathing_problem': responses[2],
        'noise_level': responses[3],
        'living_conditions': responses[4],
        'safety': responses[5],
        'basic_needs': responses[6],
        'academic_performance': responses[7],
        'study_load': responses[8],
        'teacher_student_relationship': responses[9],
        'future_career_concerns': responses[10],
        'social_support': responses[11],
        'peer_pressure': responses[12],
        'extracurricular_activities': responses[13],
        'bullying': responses[14],
        'depression': responses[15]
    }])

    # Make stress prediction
    stress_pred = stress_model.predict(features)[0]

    # Mapping for stress levels
    stress_messages = {
        0: "Minimal",
        1: "Moderate",
        2: "High"
    }

    stress = int(stress_pred)

    users_response.insert_one({
        "user": current_user.email,
        "response": {
            "mental_health_history": responses[0],
            "sleep_quality": responses[1],
            "breathing_problem": responses[2],
            "noise_level": responses[3],
            "living_conditions": responses[4],
            "safety": responses[5],
            "basic_needs": responses[6],
            "academic_performance": responses[7],
            "study_load": responses[8],
            "teacher_student_relationship": responses[9],
            "future_career_concerns": responses[10],
            "social_support": responses[11],
            "peer_pressure": responses[12],
            "extracurricular_activities": responses[13],
            "bullying": responses[14],
            "depression": responses[15],
            "stress_level": stress
        }
    })

    # Guidelines generation logic...
    guidelines = []

    # Psychological factor (mental_health_history, depression)
    if responses[0] == 1 or responses[15] > 2:
        guidelines.extend(["Praise yourself for small achievements.", "Stay positive and avoid negative thoughts."])

    # Physiological factors (sleep_quality, breathing_problem)
    if responses[1] < 3 or responses[2] > 3:
        guidelines.extend(["Improve your sleep quality.", "Avoid junk food and addictions."])

    # Environmental factors (noise_level, living_conditions, safety, basic_needs)
    if responses[3] > 3 or  responses[4] < 3 or responses[5] < 3 or responses[6] < 3:
        guidelines.extend(["Improve your living conditions and ensure your basic needs are met.", "Make sure you feel safe in your environment."])

    # Academic factors (academic_performance, study_load, teacher_student_relationship, future_career_concerns)
    if responses[7] < 4 or responses[8] > 3 or responses[9] < 3 or responses[10] > 3:
        guidelines.extend(["Organize your timetable","Stay connected with your teachers.","Pursue a career based on your interest."])

    # Social factors (social_support, peer_pressure, extracurricular_activities, bullying)
    if responses[11]<2 or  responses[12] > 3 or responses[13] <2 or responses[14] > 3:
        guidelines.extend(["Engage in extracurricular activities.","Seek help if facing bullying."])

    return jsonify({
        'stress_level': stress_messages[stress_pred],
        'guidelines': guidelines
    })

# Email Validation Function
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

if __name__ == '__main__':
    app.run(debug=True)