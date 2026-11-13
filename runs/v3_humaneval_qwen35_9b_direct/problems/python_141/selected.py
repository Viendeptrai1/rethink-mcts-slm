def file_name_check(file_name):
    if file_name.count('.') != 1:
        return 'No'
    
    parts = file_name.split('.')
    if len(parts) != 2:
        return 'No'
    
    name_part, ext_part = parts
    
    if not name_part:
        return 'No'
    
    if not name_part[0].isalpha():
        return 'No'
    
    digit_count = sum(1 for char in name_part if char.isdigit())
    if digit_count > 3:
        return 'No'
    
    valid_extensions = ['txt', 'exe', 'dll']
    if ext_part not in valid_extensions:
        return 'No'
    
    return 'Yes'