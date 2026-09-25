import re

def valid_date(date):
    # Check if the date string is empty
    if not date:
        return False
    
    # Define the regex pattern for the date format mm-dd-yyyy
    pattern = r'^(0[1-9]|1[0-2])-([0-2][0-9]|3[01])-\d{4}$'
    
    # Match the date string against the pattern
    match = re.match(pattern, date)
    if not match:
        return False
    
    # Extract month, day, and year from the matched groups
    month, day, year = map(int, match.groups())
    
    # Define the maximum days in each month
    max_days = [31, 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Check if the day is within the valid range for the given month
    if day < 1 or day > max_days[month - 1]:
        return False
    
    return True

# Test cases
print(valid_date('03-11-2000'))  # True
print(valid_date('15-01-2012'))  # False
print(valid_date('04-0-2040'))   # False
print(valid_date('06-04-2020'))  # True
print(valid_date('06/04/2020'))  # False