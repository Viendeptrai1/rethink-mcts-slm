def fix_spaces(text):
    import re
    # Replace more than two consecutive spaces with a single dash
    text = re.sub(r'\s{3,}', '-', text)
    # Replace single spaces with underscores
    text = text.replace(' ', '_')
    return text