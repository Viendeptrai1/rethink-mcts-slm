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
    
    # Check if there are more than three digits in the name
    if len(re.findall(r'\d', name)) > 3:
        return 'No'
    
    return 'Yes'

# Test cases
print(file_name_check("example.txt"))  # => 'Yes'
print(file_name_check("1example.dll")) # => 'No'
print(file_name_check("example1234.txt")) # => 'No'
print(file_name_check("example..txt")) # => 'No'
print(file_name_check("example.tx")) # => 'No'
print(file_name_check(".txt")) # => 'No'