import csv


 #Read Employees Data
employees = {}

with open("zenvy_employees.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        employees[row["employee_id"]] = {
            "name": row["employee_name"],
            "basic": int(row["base_salary"]),
            "department":row["department"],
            "designation":row["designation"]
        }


# Read Attendance Data

attendance = {}

with open("zenvy_attendance.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        attendance[row["employee_id"]] = int(float(row["overtime_hours"]))


payroll = {}
with open("zenvy_payroll.csv","r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        payroll[row["employee_id"]] ={
            "gross_salary": int(row["gross_salary"]) if row["gross_salary"] else 0,
            "tax": int(float(row["tax_deduction"])) if row["tax_deduction"] else 0,
            "pf": int(float(row["pf_deduction"])) if row["pf_deduction"] else 0,
        }

#Salary Calculation 
OVERTIME_RATE = 350

def calculate_salary(employee_id):

    try:
        if employee_id not in employees:
            raise KeyError("Employee ID not found in employees data")

        base_salary = employees[employee_id]["basic"]

        if base_salary < 0:
            raise ValueError("Base salary cannot be negative")

        overtime_hours = attendance.get(employee_id, 0)

        if overtime_hours < 0:
            raise ValueError("Overtime hours cannot be negative")

        overtime_pay = overtime_hours * OVERTIME_RATE

        gross_salary = base_salary + overtime_pay  

        tax = payroll.get(employee_id, {}).get("tax", 0)
        pf = payroll.get(employee_id, {}).get("pf", 0)

        total_deduction = tax + pf

        net_salary = gross_salary - total_deduction

        return gross_salary, total_deduction, overtime_pay, net_salary

    except Exception as e:
        print(f"Error calculating salary for {employee_id}:", e)
        return 0, 0, 0, 0
#Print Salary Output (Testing)
print("PAYROLL CALCULATION OUTPUT")
print("--------------------------")

for employee_id in payroll:
    gross, total_deduction, overtime_pay, net = calculate_salary(employee_id)

    print(
        " Emp ID:", employee_id,
        "| Dept:", employees[employee_id]["department"],
        "| Designation:",employees[employee_id]["designation"],
        "| Gross:", gross,
        "| Total Deduction:", total_deduction,
        "| Overtime Pay:", overtime_pay,
        "| Net:", net,
        
    )

#Generate Initial CSV Report
with open("Week4_payroll_report.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Emp ID",
        "Name",
        "Department",
        "Designation",
        "Gross Salary",
        "Total Deduction",
        "Overtime Pay",
        "Net Salary"
    ])

    for emp_id in employees:
        gross, total_deduction, overtime_pay, net = calculate_salary(emp_id)

        writer.writerow([
            emp_id,
            employees[emp_id]["name"],
            employees[emp_id]["department"],
            employees[emp_id]["designation"],
            gross,
            total_deduction,
            overtime_pay,
            net
        ])
        

print("\nCSV report generated: week4_payroll_report.csv")

print("\nManual Invalid ID Test")
print(calculate_salary("9999"))