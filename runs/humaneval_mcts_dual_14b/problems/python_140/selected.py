import re

def fix_spaces(text):
    # Replace sequences of 3 or more spaces with '-'
    text = re.sub(r' {3,}', '-', text)
    # Replace remaining single spaces with '_'
    text = re.sub(r' ', '_', text)
    return text