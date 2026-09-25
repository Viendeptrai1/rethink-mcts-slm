def valid_date(date):
    # Check if the date string is empty
    if not date:
        return False
    
    # Check the format of the date string
    if len(date) != 10 or date[2] != '-' or date[5] != '-':
        return False
    
    # Split the date into components
    try:
        month = int(date[:2])
        day = int(date[3:5])
        year = int(date[6:])
    except ValueError:
        return False
    
    # Check if month is valid
    if month < 1 or month > 12:
        return False
    
    # Define the number of days in each month
    days_in_month = [31, 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Check if day is valid for the given month
    if day < 1 or day > days_in_month[month - 1]:
        return False
    
    return True