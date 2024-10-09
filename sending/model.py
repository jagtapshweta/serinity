import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

# Load dataset
df = pd.read_csv('StressLevelDataset (1).csv')

# -----------------------------------
# STEP 1: Stress Level Prediction
# -----------------------------------

# Define features (X) and target variable (y_stress) for stress level
X_stress = df.drop(columns=['stress_level'])  # Exclude 'depression'
y_stress = df['stress_level']

# Split the data into 80% training and 20% testing for stress level prediction
X_train_stress, X_test_stress, y_train_stress, y_test_stress = train_test_split(
    X_stress, y_stress, test_size=0.3, random_state=42
)

# Initialize RandomForestClassifier for stress
rf_model_stress = RandomForestClassifier(random_state=42, class_weight='balanced')

# Fit the model for stress prediction
rf_model_stress.fit(X_train_stress, y_train_stress)

# Predict stress levels on the test set
y_pred_stress = rf_model_stress.predict(X_test_stress)

# Calculate and print accuracy for stress level prediction
stress_accuracy = accuracy_score(y_test_stress, y_pred_stress)
print(f"Stress Level Prediction Accuracy: {stress_accuracy:.2f}")

# Print classification report for stress level prediction
print("\nClassification Report for Stress Level Prediction:")
print(classification_report(y_test_stress, y_pred_stress))

# -----------------------------------
# STEP 2: Depression Level Prediction
# -----------------------------------

