from datetime import datetime

def valid_date(date):
    try:
        # Check if the date string is not empty
        if not date:
            return False
        
        # Parse the date string into month, day, and year
        month, day, year = map(int, date.split('-'))
        
        # Check if the month is within the valid range
        if month < 1 or month > 12:
            return False
        
        # Check if the day is within the valid range for the given month
        if month in [1, 3, 5, 7, 8, 10, 12] and (day < 1 or day > 31):
            return False
        elif month in [4, 6, 9, 11] and (day < 1 or day > 30):
            return False
        elif month == 2 and (day < 1 or day > 29):
            return False
        
        # If all checks pass, the date is valid
        return True
    
    except ValueError:
        # If parsing fails, the date is invalid
        return False