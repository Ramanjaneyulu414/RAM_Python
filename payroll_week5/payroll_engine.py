import csv
import json
import sqlite3
import logging

#Load Rules
with open("rules.json") as f:
    rules = json.load(f)

#Logging Setup
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

#Load Employees
def load_employees():
    employees = {}
    with open("zenvy_employees.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            emp_id = row["employee_id"].strip()
            if not emp_id:
                continue
            employees[emp_id] = {
                "name": row["employee_name"],
                "base_salary": int(row["base_salary"]) if row["base_salary"] else 0,
                "department": row["department"],
                "designation": row["designation"]
            }
    return employees

#Load Attendance
def load_attendance():
    attendance = {}
    with open("zenvy_attendance.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            emp_id = row["employee_id"].strip()
            if not emp_id:
                continue
            attendance[emp_id] = int(float(row["overtime_hours"])) if row["overtime_hours"] else 0
    return attendance

#Payroll Engine
class PayrollEngine:

    def __init__(self, rules):
        self.rules = rules

    def calculate(self, base_salary, overtime):
        overtime_pay = overtime * self.rules["overtime_rate"]
        gross = base_salary + overtime_pay
        tax = gross * (self.rules["tax_percentage"] / 100)
        pf = gross * (self.rules["pf_percentage"] / 100)
        net = gross - (tax + pf)
        return gross, tax, pf, net


#Run Payroll (Transaction Safe)
def run_payroll(month):

    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payroll_status(
            month TEXT PRIMARY KEY,
            status TEXT
        )
    """)

    cursor.execute("SELECT status FROM payroll_status WHERE month=?", (month,))
    record = cursor.fetchone()

    if record and record[0] == "LOCKED":
        print("Payroll already LOCKED for", month)
        return

    try:
        conn.execute("BEGIN")

        employees = load_employees()
        attendance = load_attendance()

        engine = PayrollEngine(rules)

        for emp_id in employees:
            base = employees[emp_id]["base_salary"]
            overtime = attendance.get(emp_id, 0)

            gross, tax, pf, net = engine.calculate(base, overtime)

            print(f"{emp_id} | Gross:{gross} | Net:{net}")

            logging.info(f"{emp_id} | Gross:{gross} | Net:{net}")

        cursor.execute(
            "INSERT OR REPLACE INTO payroll_status VALUES (?,?)",
            (month, "LOCKED")
        )

        conn.commit()
        print("Payroll completed & LOCKED")

    except Exception as e:
        conn.rollback()
        print("Error occurred → Rolled back")
        logging.error(str(e))

    conn.close()


#Execute
run_payroll("March")