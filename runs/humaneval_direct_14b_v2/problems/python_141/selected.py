import re

def file_name_check(file_name):
    # Check if there is exactly one dot in the file name
    if file_name.count('.') != 1:
        return 'No'
    
    # Split the file name into name and extension
    name, extension = file_name.split('.')
    
    # Check if the extension is valid
    if extension not in ['txt', 'exe', 'dll']:
        return 'No'
    
    # Check if the name is not empty and starts with a letter
    if not name or not name[0].isalpha():
        return 'No'
    
    # Count the number of digits in the name
    digit_count = sum(c.isdigit() for c in name)
    
    # Check if there are more than three digits
    if digit_count > 3:
        return 'No'
    
    return 'Yes'