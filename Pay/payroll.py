import pandas as pd
from flask import Flask, jsonify

#Load CSV files
employees = pd.read_csv("zenvy_employees_new.csv")
print(employees.columns)
attendance = pd.read_csv("zenvy_attendance_new.csv")

#Merge data
data = pd.merge(employees, attendance, on="employee_id")

#Dummy salary add
data["salary"] = 30000

#Salary calculation
data["per_day_salary"] = data["salary"] / 30
data["final_salary"] = data["per_day_salary"] * data["days_present"]

# BONUS (optional)
#data["bonus"] = 1000
#data["final_salary"] = data["final_salary"] + data["bonus"]


data["leaves"] = 30 - data["days_present"]

data = data[[
    "name",
    "role",
    "employee_id",
    "final_salary",
    "days_present",
    "leaves",
    "per_day_salary",
    "salary"
]]

# Save output
data.to_csv("final_salary_output.csv", index=False)

print("✅ Salary calculated successfully")
print(data[["employee_id", "final_salary"]])

#Create API
app = Flask(__name__)

@app.route("/")
def home():
    return "Payroll API Running"

@app.route("/salary")
def salary():
    return jsonify(data.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)