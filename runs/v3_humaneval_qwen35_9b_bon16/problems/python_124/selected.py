import re

def valid_date(date):
    """You have to write a function which validates a given date string and
    returns True if the date is valid otherwise False.
    The date is valid if all of the following rules are satisfied:
    1. The date string is not empty.
    2. The number of days is not less than 1 or higher than 31 days for months 1,3,5,7,8,10,12. And the number of days is not less than 1 or higher than 30 days for months 4,6,9,11. And, the number of days is not less than 1 or higher than 29 for the month 2.
    3. The months should not be less than 1 or higher than 12.
    4. The date should be in the format: mm-dd-yyyy

    for example: 
    valid_date('03-11-2000') => True

    valid_date('15-01-2012') => False

    valid_date('04-0-2040') => False

    valid_date('06-04-2020') => True

    valid_date('06/04/2020') => False
    """
    if not date or not isinstance(date, str):
        return False

    # Check format strictly: mm-dd-yyyy with exactly two digits for each part
    pattern = r'^(\d{2})-(\d{2})-(\d{4})$'
    match = re.match(pattern, date)
    
    if not match:
        return False
    
    month_str, day_str, year_str = match.groups()
    
    month = int(month_str)
    day = int(day_str)
    
    # Rule 3: Month should be between 1 and 12
    if month < 1 or month > 12:
        return False
    
    # Rule 2: Validate days based on month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        max_day = 31
    elif month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        max_day = 29
    else:
        return False
    
    if day < 1 or day > max_day:
        return False
    
    return True