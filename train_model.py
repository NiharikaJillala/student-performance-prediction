import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Illustrative sample data for this classroom demonstration.
# result: 1 = Likely to Pass, 0 = Needs Improvement.
data = {
    "study_hours": [1,2,3,4,5,6,7,8,2,3,5,6,1,4,7,8,2,5,6,3,9,10,4,1,7,5,8,2,6,3,9,4,5,7,2,8,6,1,10,3],
    "attendance": [45,55,60,65,75,80,90,95,50,62,78,85,40,70,92,98,58,76,88,63,96,98,72,42,89,74,94,52,83,61,97,68,79,91,56,96,86,38,99,64],
    "previous_marks": [35,42,50,55,68,72,85,90,40,52,70,78,30,60,88,94,45,67,80,53,96,98,62,32,86,66,92,43,76,51,97,58,73,89,47,95,82,28,99,54],
    "assignment_marks": [30,40,48,58,65,75,82,95,38,50,72,80,25,62,90,96,42,68,84,55,98,96,64,28,88,70,94,45,79,52,99,60,76,91,49,97,85,22,98,57],
    "result": [0,0,0,0,1,1,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,0,1,1,0,1,0]
}

df = pd.DataFrame(data)

# Save the dataset as a CSV file.
df.to_csv("students.csv", index=False)

features = [
    "study_hours",
    "attendance",
    "previous_marks",
    "assignment_marks"
]
X = df[features]
y = df["result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Train a Decision Tree classification model.
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model on the held-out test portion.
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# Save the trained model so Flask can load it.
joblib.dump(model, "model.pkl")

print("Dataset created: students.csv")
print("Trained model saved: model.pkl")
print(f"Test accuracy on this small illustrative dataset: {accuracy * 100:.1f}%")
print(classification_report(y_test, predictions, zero_division=0))
print("You can now run: python app.py")
