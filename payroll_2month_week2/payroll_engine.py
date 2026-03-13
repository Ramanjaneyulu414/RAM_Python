import csv
import sqlite3
import logging

from salary_structure import calculate_salary_structure
from compliance_engine import calculate_compliance
from payslip_generator import generate_payslip


# ---------- Logging Setup ----------
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ---------- Load Employees ----------
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


# ---------- Load Attendance ----------
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


# ---------- Run Payroll ----------
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

        for emp_id in employees:

            name = employees[emp_id]["name"]
            base_salary = employees[emp_id]["base_salary"]
            overtime = attendance.get(emp_id, 0)

            # Salary Structure
            structure = calculate_salary_structure(base_salary)

            basic = structure["basic"]
            hra = structure["hra"]
            bonus = structure["bonus"]
            gross = structure["gross"]

            # Compliance Calculation
            compliance = calculate_compliance(gross, basic)

            deductions = compliance["total_deductions"]

            net_salary = gross - deductions

            print(f"{emp_id} | Gross:{gross} | Net:{net_salary}")

            logging.info(f"{emp_id} | Gross:{gross} | Net:{net_salary}")

            # Generate Payslip
            generate_payslip(
                emp_id,
                name,
                basic,
                hra,
                bonus,
                net_salary
            )

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


# ---------- Execute ----------
run_payroll("March")