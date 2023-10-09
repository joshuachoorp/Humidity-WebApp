from jinja2 import Environment

def month_name_filter(month_number):
    months = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    return months[month_number - 1]  # Adjust month number to match list index (starting from 0)

