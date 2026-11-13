import re

def valid_date(date):
    # Rule 1: The date string is not empty
    if not date or not date.strip():
        return False

    # Rule 4: The date should be in the format: mm-dd-yyyy
    pattern = r'^(\d{2})-(\d{2})-(\d{4})$'
    match = re.match(pattern, date)
    
    if not match:
        return False

    month_str, day_str, year_str = match.groups()

    # Convert to integers
    month = int(month_str)
    day = int(day_str)
    year = int(year_str)

    # Rule 3: The months should not be less than 1 or higher than 12
    if month < 1 or month > 12:
        return False

    # Rule 2: Validate days based on month
    # Months with 31 days: 1, 3, 5, 7, 8, 10, 12
    # Months with 30 days: 4, 6, 9, 11
    # Month 2 has max 29 days (as per problem statement, no leap year logic specified beyond 29)
    
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day < 1 or day > 31:
            return False
    elif month in [4, 6, 9, 11]:
        if day < 1 or day > 30:
            return False
    elif month == 2:
        if day < 1 or day > 29:
            return False
    else:
        # This case is already covered by month < 1 or month > 12 check,
        # but kept for logical completeness if month validation was separate
        return False

    return True