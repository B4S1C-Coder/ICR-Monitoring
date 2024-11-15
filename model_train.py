import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

scaler = StandardScaler()

data = pd.read_csv('smart_grid_stability_augmented.csv')

print("Duplicate rows:", data.duplicated().sum())
# Check correlation between features and target
#print(data.corr()['stab'])
print(data['stab'].value_counts())

x = data.drop(['stab', 'stabf'], axis=1)
y = data['stab'].apply(lambda x: 1 if x == 'stable' else 0)

x_scaled = scaler.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.9, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(accuracy_score(y_test, y_pred))
