def file_name_check(file_name):
    if '.' not in file_name:
        return 'No'
    
    parts = file_name.split('.')
    if len(parts) != 2:
        return 'No'
    
    prefix, suffix = parts
    
    if not prefix:
        return 'No'
    
    if not prefix[0].isalpha():
        return 'No'
    
    if suffix not in ['txt', 'exe', 'dll']:
        return 'No'
    
    digit_count = sum(1 for char in file_name if char.isdigit())
    if digit_count > 3:
        return 'No'
    
    return 'Yes'