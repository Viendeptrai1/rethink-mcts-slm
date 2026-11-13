import re

def file_name_check(file_name):
    pattern = r'^[a-zA-Z][^0-9]*\d{0,3}[^0-9]*\.[txt|exe|dll]{3}$'
    return 'Yes' if re.match(pattern, file_name) else 'No'