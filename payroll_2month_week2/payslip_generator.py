from reportlab.pdfgen import canvas

def generate_payslip(emp_id, name, basic, hra, bonus, net):

    file_name = f"payslip_{emp_id}.pdf"

    c = canvas.Canvas(file_name)

    c.drawString(100,750,f"Employee ID: {emp_id}")
    c.drawString(100,730,f"Name: {name}")

    c.drawString(100,700,f"Basic: {basic}")
    c.drawString(100,680,f"HRA: {hra}")
    c.drawString(100,660,f"Bonus: {bonus}")

    c.drawString(100,620,f"Net Salary: {net}")

    c.save()