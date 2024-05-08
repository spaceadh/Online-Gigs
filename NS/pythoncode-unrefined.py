import pandas as pd

# Define column names based on the dataset's documentation
column_names = [
    "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
    "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
    "hours-per-week", "native-country", "class"
]

# Load the dataset with specified column names and handle initial spaces in the column names
data = pd.read_csv("path_to_your_data/adult.data", header=None, names=column_names, skipinitialspace=True)

# Display the first few rows of the dataset to understand its structure
print(data.head())

# Check for missing values in the dataset
missing_values = data.isnull().sum()
print("Missing Values:\n", missing_values)

# Handle missing values
data.dropna(inplace=True)

# Check for outliers and anomalies in numerical columns using descriptive statistics
numerical_cols = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
print("Descriptive Statistics for Numerical Columns:")
print(data[numerical_cols].describe())

# Handle outliers using z-score or IQR method for numerical columns
# Example using z-score for 'age' column
from scipy.stats import zscore
data['age_zscore'] = zscore(data['age'])
data = data[(data['age_zscore'] < 3) & (data['age_zscore'] > -3)]

# Drop the temporary z-score column after handling outliers
data.drop('age_zscore', axis=1, inplace=True)

# Verify if outliers are handled
print("Descriptive Statistics after handling outliers:")
print(data[numerical_cols].describe())

import matplotlib.pyplot as plt
import seaborn as sns

# Perform EDA
# Example: histogram for age distribution
plt.figure(figsize=(8, 6))
sns.histplot(data['age'], bins=30, kde=True)
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Age Distribution')
plt.show()

# Correlation Analysis: Visualizing correlation between numerical features
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# Pair Plot: Visualizing relationships between numerical features
sns.pairplot(data[numerical_cols])
plt.suptitle('Pair Plot for Numerical Features', y=1.02)
plt.show()

# Box Plot: Visualizing distribution of numerical features across income classes
plt.figure(figsize=(12, 8))
sns.boxplot(x='class', y='age', data=data)
plt.xlabel('Income Class')
plt.ylabel('Age')
plt.title('Age Distribution across Income Classes')
plt.show()

# Bar Plot: Visualizing distribution of categorical features
plt.figure(figsize=(10, 6))
sns.countplot(x='education', hue='class', data=data)
plt.xlabel('Education Level')
plt.ylabel('Count')
plt.title('Distribution of Education Level across Income Classes')
plt.xticks(rotation=45)
plt.legend(title='Income Class')
plt.show()

# Violin Plot: Visualizing distribution of numerical features across income classes
plt.figure(figsize=(12, 8))
sns.violinplot(x='class', y='hours-per-week', data=data)
plt.xlabel('Income Class')
plt.ylabel('Hours per Week')
plt.title('Distribution of Hours per Week across Income Classes')
plt.show()

# Scatter Plot: Visualizing relationship between numerical features
plt.figure(figsize=(10, 8))
sns.scatterplot(x='age', y='capital-gain', hue='class', data=data)
plt.xlabel('Age')
plt.ylabel('Capital Gain')
plt.title('Scatter Plot: Age vs Capital Gain (colored by Income Class)')
plt.legend(title='Income Class')
plt.show()

# Additional EDA tasks can be added as needed, such as facet grids, line plots, etc.

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Assuming categorical_cols and numerical_cols are defined earlier
# categorical_cols = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country"]
# numerical_cols = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]

# One-hot encode categorical variables
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Optionally scale numerical features
scaler = MinMaxScaler()
data_encoded[numerical_cols] = scaler.fit_transform(data_encoded[numerical_cols])

# Create new features if required
data_encoded['gov_employment'] = data_encoded['workclass_Federal-gov'] | data_encoded['workclass_Local-gov']

# Print the new column and its values
print(data_encoded['gov_employment'])

# Check the engineered features and updated dataset
print(data_encoded.head())

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Define a ColumnTransformer for one-hot encoding
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), categorical_cols)],
    remainder='passthrough'  # Pass through numerical columns as-is
)

# Fit and transform the data using the ColumnTransformer
X_train_encoded = preprocessor.fit_transform(X_train)
X_test_encoded = preprocessor.transform(X_test)

# Initialize and train the Random Forest Classifier using the encoded data
model = RandomForestClassifier(random_state=42)
model.fit(X_train_encoded, y_train)

# Make predictions
y_pred = model.predict(X_test_encoded)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))

