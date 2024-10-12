from flask import Flask, request, jsonify, render_template,session,redirect,url_for,flash
import pandas as pd
import joblib
from flask_cors import CORS
from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt 
import re


app = Flask(__name__)
CORS(app) 
app.secret_key="Serenity"


client = MongoClient('mongodb+srv://jagtapshweta26:tJy5x6QpWUPt7lEX@serenity.r68xx.mongodb.net/')
db = client['Serenity']
questions_collection = db['Questions']
users_collection = db['Users']
users_response = db['Responses']

@app.route('/chat-bot.html/questions', methods=['GET'])
def get_questions():
    questions = list(questions_collection.find({}, {'_id': 0}))  # Retrieve without MongoDB ObjectID
    return jsonify(questions)

stress_model = joblib.load('../model_stress.pkl')

@app.route('/')
def home():
    return render_template('index.html',userName=session.get("userName",""),isLogged=session.get("isLogged",False))  


def is_valid_email(email):
    """Validate email format using regular expression."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    """Check password against constraints."""
    return (len(password) >= 8 and  
            re.search(r"[A-Z]", password) and  
            re.search(r"[a-z]", password) and  
            re.search(r"[0-9]", password) and  
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))  

@app.route('/login', methods=["POST"])
def login():
    userName = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    if not is_valid_email(email):
        flash("Invalid email format.")

    if not is_valid_password(password):
        flash("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a digit, and a special character.")

    existing_user = users_collection.find_one({"email": email})

    if existing_user:
        if bcrypt.checkpw(password.encode('utf-8'), existing_user["password"]):
            session["isLogged"] = True
            session["userName"] = existing_user["name"]  
            session["email"] = email
            return redirect(url_for("home"))
        else:
            flash("Incorrect password, please try again.")
        return redirect(url_for("home"))
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_collection.insert_one({
            "name": userName,
            "email": email,
            "password": hashed_password 
        })
        session["isLogged"] = True
        session["userName"] = userName
        session["email"] = email
        return redirect(url_for("home")) 


@app.route('/log-out', methods=['POST'])
def logOut():
    session.clear() 
    return redirect(url_for("home"))


@app.route('/chat-bot.html')
def chatBot():
    return render_template('chat-bot.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json 
    responses = data['responses']

    users_response.insert_one({
        "user": session["email"],
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
            "depression": responses[15]
        }
    })


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

    # Prepare guidelines based on responses
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

if __name__ == '__main__':
    app.run(debug=True)
