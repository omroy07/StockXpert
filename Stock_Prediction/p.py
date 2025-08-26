import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Folder containing all cleaned CSVs
folder_path = r"D:\MLPROJECTS\MoneyVest1\companydataset\cleaned"
all_data = []
   
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path)

            # Ensure required columns exist
            required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in df.columns for col in required_cols):
                print(f"Skipping {file} — missing one or more required columns.")
                continue

            # Sort by date
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])
            df = df.sort_values('Date')

            # Create target column: 1 if next day's Close > today's Close
            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Target']].dropna()

            all_data.append(df)

        except Exception as e:
            print(f"Error reading {file}: {e}")

# Combine all valid company data
if not all_data:
    raise ValueError("No valid CSVs found in the folder.")

combined_df = pd.concat(all_data, ignore_index=True)
print("Total rows after combining:", combined_df.shape[0])

# Features and target
X = combined_df[['Open', 'High', 'Low', 'Close', 'Volume']]
y = combined_df['Target']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", round(accuracy * 100, 2), "%")

# Save model
joblib.dump(model, "stock_predictor.pkl")
print("Model saved to stock_predictor.pkl")
