import re

def fix_spaces(text):
    # Replace more than 2 consecutive spaces with a single dash
    text = re.sub(r'\s{3,}', '-', text)
    # Replace single spaces with underscores
    text = re.sub(r'\s', '_', text)
    return text