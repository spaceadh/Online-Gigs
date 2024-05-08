import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Kaggle-Appointment.csv')

print(df.columns)

print(df.head())
# Display information about the dataset

print(df.info())

# Display summary statistics
print(df.describe())

# Check for missing values
print("Missing values:\n", df.isnull().sum())

# Check the distribution of the target variable 'No-show'
print("Distribution of 'No-show':\n", df['No-show'].value_counts())

# Data Preprocessing
# Convert 'No-show' column to binary (1 for 'Yes' and 0 for 'No')
df['No-show'] = df['No-show'].apply(lambda x: 1 if x == 'Yes' else 0)

# Drop unnecessary columns like PatientId, AppointmentID, and Neighbourhood
df.drop(['PatientId', 'AppointmentID', 'Neighbourhood'], axis=1, inplace=True)

# Handle categorical variables
label_encoders = {}
for col in df.select_dtypes(include=['object']).columns:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Split the dataset into features and target variable
X = df.drop('No-show', axis=1)
y = df['No-show']

# Split the df into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model 1: Logistic Regression
logreg_model = LogisticRegression(random_state=42)
logreg_model.fit(X_train_scaled, y_train)
logreg_y_pred = logreg_model.predict(X_test_scaled)
logreg_accuracy = accuracy_score(y_test, logreg_y_pred)
logreg_roc_auc = roc_auc_score(y_test, logreg_model.predict_proba(X_test_scaled)[:, 1])

# Model 2: Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
rf_y_pred = rf_model.predict(X_test_scaled)
rf_accuracy = accuracy_score(y_test, rf_y_pred)
rf_roc_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test_scaled)[:, 1])

# Model Comparison
print("Model Comparison:")
print(f"Logistic Regression Accuracy: {logreg_accuracy}")
print(f"Logistic Regression ROC-AUC: {logreg_roc_auc}")
print(f"Random Forest Accuracy: {rf_accuracy}")
print(f"Random Forest ROC-AUC: {rf_roc_auc}")

# Plot ROC curves for both models
logreg_fpr, logreg_tpr, _ = roc_curve(y_test, logreg_model.predict_proba(X_test_scaled)[:, 1])
rf_fpr, rf_tpr, _ = roc_curve(y_test, rf_model.predict_proba(X_test_scaled)[:, 1])

plt.figure(figsize=(8, 6))
plt.plot(logreg_fpr, logreg_tpr, label='Logistic Regression')
plt.plot(rf_fpr, rf_tpr, label='Random Forest Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
