from datetime import date

def calculate(input_form):
    today = date.today()
    value = (input_form - today).days
    return value