import re

def valid_date(date):
    # Check if the date string is empty
    if not date:
        return False
    
    # Check if the date matches the format mm-dd-yyyy
    if not re.match(r'^\d{2}-\d{2}-\d{4}$', date):
        return False
    
    # Split the date into month, day, and year
    month, day, year = map(int, date.split('-'))
    
    # Check if the month is within the valid range
    if month < 1 or month > 12:
        return False
    
    # Check if the day is within the valid range for each month
    if month in {1, 3, 5, 7, 8, 10, 12}:
        if day < 1 or day > 31:
            return False
    elif month in {4, 6, 9, 11}:
        if day < 1 or day > 30:
            return False
    elif month == 2:
        # Check for leap year
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            if day < 1 or day > 29:
                return False
        else:
            if day < 1 or day > 28:
                return False
    else:
        return False
    
    return True