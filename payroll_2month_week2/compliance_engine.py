def calculate_compliance(gross, basic):

    pf = basic * 0.12

    if gross <= 21000:
        esi = gross * 0.0075
    else:
        esi = 0

    if gross > 15000:
        professional_tax = 200
    else:
        professional_tax = 0

    deductions = pf + esi + professional_tax

    return {
        "pf": pf,
        "esi": esi,
        "pt": professional_tax,
        "total_deductions": deductions
        }