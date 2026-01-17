import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

os.makedirs("app/services", exist_ok=True)

np.random.seed(42)
n_samples = 2000

incomes = np.random.randint(0, 40000, n_samples)
family_sizes = np.random.randint(1, 12, n_samples)

risks = []
for income, size in zip(incomes, family_sizes):
    if income > 25000:
        risks.append(1)
    elif income > 10000 and size < 3:
        risks.append(1)
    else:
        risks.append(0)

df = pd.DataFrame({
    'total_income': incomes,
    'family_size': family_sizes,
    'risk_label': risks
})

X = df[['total_income', 'family_size']]
y = df['risk_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

joblib.dump(rf_model, 'app/services/risk_model.pkl')
print("Random Forest Model trained and saved successfully.")