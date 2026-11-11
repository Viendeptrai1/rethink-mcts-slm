def fix_spaces(text):
    result = []
    i = 0
    while i < len(text):
        if text[i] == ' ':
            space_count = 0
            while i < len(text) and text[i] == ' ':
                space_count += 1
                i += 1
            if space_count > 2:
                result.append('-')
            else:
                result.extend(['_'] * space_count)
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)