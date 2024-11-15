import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Step 1: Load the dataset from CSV
data = pd.read_csv('smart_grid_stability_augmented.csv')  # Update the path to your CSV file if needed

# Step 2: Prepare the features (X) and target (y)
X = data.drop(['stab', 'stabf'], axis=1)  # Features: drop the target columns
y = data['stabf']  # Use original 'stab' values ('stable'/'unstable')

# Step 3: Scale the features (important for most machine learning models)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Load the pre-trained model using joblib
model = joblib.load('gridModel.pkl')  # Replace with the path to your saved model

# Step 5: Make predictions using the model
y_pred = model.predict(X_scaled)

print(y)

# Step 6: Calculate the accuracy of the model
accuracy = accuracy_score(y, y_pred)

print(f"Accuracy of the model on the dataset: {accuracy:.4f}")

