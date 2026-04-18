import pandas as pd
from flask import Flask
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph
employees = pd.read_csv("zenvy_employees_new.csv")
attendance = pd.read_csv("zenvy_attendance_new.csv")
data = pd.merge(employees, attendance, on="employee_id")

#salary
data["salary"] = 30000
data["basic"] = data["salary"]
data["hra"] = data["basic"] * 0.2
data["bonus"] = 1000

#Deductions
data["pf"] = data["basic"] * 0.1
data["tax"] = data["basic"] * 0.05

#Calculation
data["gross_salary"] = data["basic"] + data["hra"] + data["bonus"]
data["total_deductions"] = data["pf"] + data["tax"]
data["net_salary"] = data["gross_salary"] - data["total_deductions"]

#Columns
data = data[[
    "name",
    "role",
    "employee_id",
    "basic",
    "hra",
    "bonus",
    "pf",
    "tax",
    "gross_salary",
    "total_deductions",
    "net_salary"
]]

#Output
data.to_csv("week4_salary_output.csv", index=False)

print("Week 4 Salary calculated successfully")
print(data[["employee_id", "net_salary"]])

#PDF Payslip 
def generate_payslip(emp):
    pdf = SimpleDocTemplate(f"{emp['name']}_payslip.pdf")
    content = []

    content.append(Paragraph(f"Name: {emp['name']}"))
    content.append(Paragraph(f"Role: {emp['role']}"))
    content.append(Paragraph(f"Basic: {emp['basic']}"))
    content.append(Paragraph(f"HRA: {emp['hra']}"))
    content.append(Paragraph(f"Bonus: {emp['bonus']}"))
    content.append(Paragraph(f"PF: {emp['pf']}"))
    content.append(Paragraph(f"Tax: {emp['tax']}"))
    content.append(Paragraph(f"Net Salary: {emp['net_salary']}"))

    pdf.build(content)

# Generate payslips
for _, row in data.iterrows():
    generate_payslip(row)

# Flask API
app = Flask(__name__)

@app.route("/")
def home():
    return "Week 4 Payroll API Running"

@app.route("/salary")
def salary():
    return json.dumps(data.to_dict(orient="records"), indent=4)

if __name__ == "__main__":
    app.run(debug=False)