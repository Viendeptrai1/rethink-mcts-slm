def fix_spaces(text):
    if not text:
        return text
    
    result = []
    i = 0
    n = len(text)
    
    while i < n:
        if text[i] == ' ':
            count = 0
            while i < n and text[i] == ' ':
                count += 1
                i += 1
            
            if count <= 2:
                result.append('_' * count)
            else:
                result.append('-')
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)