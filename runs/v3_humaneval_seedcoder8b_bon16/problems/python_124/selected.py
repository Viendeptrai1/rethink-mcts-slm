def valid_date(date):
    if not date or len(date) != 10:
        return False

    parts = date.split('-')
    if len(parts) != 3:
        return False

    try:
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])
    except ValueError:
        return False

    if month < 1 or month > 12:
        return False
    if day < 1:
        return False

    if month in [1, 3, 5, 7, 8, 10, 12]:
        return day <= 31
    elif month in [4, 6, 9, 11]:
        return day <= 30
    elif month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return day <= 29
        else:
            return day <= 28
    else:
        return False