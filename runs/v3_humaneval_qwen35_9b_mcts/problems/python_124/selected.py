import re

def valid_date(date):
    if not date:
        return False
    
    # Check format strictly: mm-dd-yyyy using regex
    pattern = r'^(\d{2})-(\d{2})-(\d{4})$'
    match = re.match(pattern, date)
    
    if not match:
        return False
    
    month_str, day_str, year_str = match.groups()
    
    try:
        month = int(month_str)
        day = int(day_str)
        year = int(year_str)
    except ValueError:
        return False
    
    # Rule 3: Month must be between 1 and 12
    if month < 1 or month > 12:
        return False
    
    # Rule 1: Date string not empty (already checked at start)
    # Rule 2: Day validation based on month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day < 1 or day > 31:
            return False
    elif month in [4, 6, 9, 11]:
        if day < 1 or day > 30:
            return False
    elif month == 2:
        if day < 1 or day > 29:
            return False
    
    return True