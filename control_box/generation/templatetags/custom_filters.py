from django import template
import re

register = template.Library()

@register.filter
def month_name(value):
    month_map = {
        "1": "январь", "2": "февраль", "3": "март",
        "4": "апрель", "5": "май", "6": "июнь",
        "7": "июль", "8": "август", "9": "сентябрь",
        "10": "октябрь", "11": "ноябрь", "12": "декабрь"
    }
    
    # Если список
    if isinstance(value, list):
        months = []
        for item in value:
            months.append(month_map.get(str(item), item))
        return " - ".join(months)
    
    # Если строка с несколькими числами
    if isinstance(value, str):
        numbers = re.findall(r'\d+', value)
        if len(numbers) > 1:
            months = [month_map.get(num, num) for num in numbers]
            return " | ".join(months)
        elif numbers:
            return month_map.get(numbers[0], value)
    
    return month_map.get(str(value), value)


@register.filter
def weekly_name(value):
    weekly_map = {
        "0": "понедельник", "1": "вторник", "2": "среда",
        "3": "четверг", "4": "пятница", "5": "суббота",
        "6": "воскресенье"
    }
    
    # Если список
    if isinstance(value, list):
        months = []
        for item in value:
            months.append(weekly_map.get(str(item), item))
        return " - ".join(months)
    
    # Если строка с несколькими числами
    if isinstance(value, str):
        numbers = re.findall(r'\d+', value)
        if len(numbers) > 1:
            months = [weekly_map.get(num, num) for num in numbers]
            return " | ".join(months)
        elif numbers:
            return weekly_map.get(numbers[0], value)
    
    return weekly_map.get(str(value), value)