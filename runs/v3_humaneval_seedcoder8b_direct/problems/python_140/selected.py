def fix_spaces(text):
    result = []
    space_count = 0
    for char in text:
        if char == ' ':
            space_count += 1
            if space_count > 2:
                result.append('-')
        else:
            if space_count > 0:
                if space_count == 1:
                    result.append('_')
                space_count = 0
            result.append(char)
    
    if space_count > 0:
        if space_count == 1:
            result.append('_')
    
    return ''.join(result)