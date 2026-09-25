import re

def valid_date(date):
    """Validates a given date string and returns True if the date is valid otherwise False."""
    
    # Step 1: Check if the input date string is empty
    if not date:
        return False
    
    # Step 2: Define the regex pattern for the date format mm-dd-yyyy
    pattern = r'^(0[1-9]|1[0-2])-([0-2][0-9]|3[01])-\d{4}$'
    
    # Step 3: Use regex to check if the date matches the pattern
    if not re.match(pattern, date):
        return False
    
    # Step 4: Extract month, day, and year from the date string
    month, day, year = map(int, date.split('-'))
    
    # Step 5: Check the number of days in each month
    if month in {1, 3, 5, 7, 8, 10, 12}:
        if not (1 <= day <= 31):
            return False
    elif month in {4, 6, 9, 11}:
        if not (1 <= day <= 30):
            return False
    elif month == 2:
        if not (1 <= day <= 29):
            return False
    
    # Step 6: If all checks pass, the date is valid
    return True

# Example usage:
# print(valid_date('03-11-2000'))  # True
# print(valid_date('15-01-2012'))  # False
# print(valid_date('04-0-2040'))   # False
# print(valid_date('06-04-2020'))  # True
# print(valid_date('06/04/2020'))  # False