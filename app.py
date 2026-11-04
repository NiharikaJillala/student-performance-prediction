
from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Project file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "model.pkl")
DATA_FILE = os.path.join(BASE_DIR, "students.csv")

# Load the trained machine learning model
model = joblib.load(MODEL_FILE)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input values from the website form
        study_hours = float(request.form["study_hours"])
        attendance = float(request.form["attendance"])
        previous_marks = float(request.form["previous_marks"])
        assignment_marks = float(request.form["assignment_marks"])

        # Validate input values
        if not 0 <= study_hours <= 24:
            return "Study hours must be between 0 and 24."

        if not 0 <= attendance <= 100:
            return "Attendance must be between 0 and 100."

        if not 0 <= previous_marks <= 100:
            return "Previous marks must be between 0 and 100."

        if not 0 <= assignment_marks <= 100:
            return "Assignment marks must be between 0 and 100."

        # Prepare input for prediction
        input_data = pd.DataFrame(
            [[study_hours, attendance, previous_marks, assignment_marks]],
            columns=[
                "study_hours",
                "attendance",
                "previous_marks",
                "assignment_marks"
            ]
        )

        # Predict student performance
        prediction = model.predict(input_data)[0]

        # Convert prediction into readable text
        if prediction == 1:
            result = "Likely to Pass"
        else:
            result = "Needs Improvement"

        return render_template(
            "result.html",
            prediction=result,
            study_hours=study_hours,
            attendance=attendance,
            previous_marks=previous_marks,
            assignment_marks=assignment_marks
        )

    except ValueError:
        return "Please enter valid numbers in all fields."

    except Exception as error:
        return f"An error occurred: {error}"


@app.route("/analysis")
def analysis():
    # Read student dataset
    data = pd.read_csv(DATA_FILE)

    # Calculate basic statistics
    total_students = len(data)
    average_marks = round(data["previous_marks"].mean(), 2)
    average_attendance = round(data["attendance"].mean(), 2)

    # Count students in each performance category
    pass_count = int((data["result"] == 1).sum())
    fail_count = int((data["result"] == 0).sum())

    return render_template(
        "analysis.html",
        total_students=total_students,
        average_marks=average_marks,
        average_attendance=average_attendance,
        pass_count=pass_count,
        fail_count=fail_count
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
