from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the pre-trained model for stress prediction
stress_model = joblib.load('../model_stress.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the JSON data from the request

    # Prepare the features from the responses
    responses = data['responses']

    # Create a DataFrame with named columns corresponding to your model
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
        0: "Looks like you have minimal stress and you are fine to go! Stay like this forever!",
        1: "Your stress level seems at an intermediate level, you need to follow certain guidelines which I am providing.",
        2: "Your stress analysis tells me that you are in high stress! You must consult with a counsellor."
    }

    # Prepare guidelines based on responses
    guidelines = []

    # Psychological factor (mental_health_history, depression)
    if responses[0] == 1 or responses[15] > 2:
        guidelines.append(" Praise yourself for small achievements.  Stay positive and avoid negative thoughts.")

    # Physiological factors (sleep_quality, breathing_problem)
    if responses[1] < 3 or responses[2] > 3:
        guidelines.append("1. Improve your sleep quality. 2. Avoid junk food and addictions.")

    # Environmental factors (noise_level, living_conditions, safety, basic_needs)
    if responses[3] > 3 or  responses[4] < 3 or responses[5] < 3 or responses[6] < 3:
        guidelines.append("1. Improve your living conditions and ensure your basic needs are met. 2. Make sure you feel safe in your environment.")

    # Academic factors (academic_performance, study_load, teacher_student_relationship, future_career_concerns)
    if responses[7] < 4 or responses[8] > 3 or responses[9] < 3 or responses[10] > 3:
        guidelines.append("1. Organize your timetable. 2. Stay connected with your teachers. 3. Pursue a career based on your interest.")

    # Social factors (social_support, peer_pressure, extracurricular_activities, bullying)
    if responses[11]<2 or  responses[12] > 3 or responses[13] <2 or responses[14] > 3:
        guidelines.append("1. Engage in extracurricular activities. 2. Seek help if facing bullying.")

    return jsonify({
        'stress_level': stress_messages[stress_pred],
        'guidelines': guidelines
    })

if __name__ == '__main__':
    app.run(debug=True)
