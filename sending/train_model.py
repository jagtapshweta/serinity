import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the normalized dataset
data = pd.read_csv('StressLevelDataset (1).csv')

# Prepare features and target variable for stress level prediction
feature_columns = [
    'mental_health_history', 'sleep_quality', 'breathing_problem', 
    'noise_level', 'living_conditions', 'safety', 
    'basic_needs', 'academic_performance', 'study_load', 
    'teacher_student_relationship', 'future_career_concerns', 
    'social_support', 'peer_pressure', 'extracurricular_activities', 
    'bullying', 'depression'  # Include depression as a feature
]

# Check if all feature columns are in the dataset
for col in feature_columns:
    if col not in data.columns:
        raise ValueError(f"Column '{col}' not found in the dataset.")

# Feature matrix (X) and target variable (y_stress)
X = data[feature_columns]
y_stress = data['stress_level']

# Split the dataset into training and testing sets
X_train, X_test, y_train_stress, y_test_stress = train_test_split(X, y_stress, test_size=0.2, random_state=42)

# Train Random Forest Classifier for stress level prediction
stress_model = RandomForestClassifier(n_estimators=100, random_state=42)
stress_model.fit(X_train, y_train_stress)

# Save the model for stress level prediction
with open('model_stress.pkl', 'wb') as f:
    pickle.dump(stress_model, f)

print("Stress level prediction model saved successfully.")
