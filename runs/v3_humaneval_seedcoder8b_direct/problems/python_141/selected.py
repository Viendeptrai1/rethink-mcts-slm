def file_name_check(file_name):
    parts = file_name.split('.')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return 'No'
    
    if not parts[0][0].isalpha():
        return 'No'
    
    if sum(c.isdigit() for c in file_name) > 3:
        return 'No'
    
    if parts[1] not in ['txt', 'exe', 'dll']:
        return 'No'
    
    return 'Yes'