from datetime import datetime

def valid_date(date):
    if len(date) != 10 or date[2] != '-' or date[5] != '-':
        return False
    
    try:
        month, day, year = map(int, date.split('-'))
    except ValueError:
        return False
    
    if month < 1 or month > 12 or day < 1:
        return False
    
    if month == 2 and (day < 1 or day > 29):
        return False
    elif month in [4, 6, 9, 11] and (day < 1 or day > 30):
        return False
    elif day > 31:
        return False
    
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False