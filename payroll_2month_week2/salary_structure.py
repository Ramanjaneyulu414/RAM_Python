def calculate_salary_structure(ctc):

    basic = ctc * 0.50
    hra = ctc * 0.30
    bonus = ctc * 0.10

    gross = basic + hra + bonus

    return {
        "basic": basic,
        "hra": hra,
        "bonus": bonus,
        "gross": gross
    }