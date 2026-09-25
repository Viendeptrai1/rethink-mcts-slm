import re

def fix_spaces(text):
    # Replace all occurrences of more than 2 consecutive spaces with '-'
    text = re.sub(r' {3,}', '-', text)
    # Replace all remaining single or double spaces with '_'
    text = re.sub(r' {1,2}', '_', text)
    return text

# Test cases
print(fix_spaces("Example"))        # Output: "Example"
print(fix_spaces("Example 1"))      # Output: "Example_1"
print(fix_spaces(" Example 2"))     # Output: "_Example_2"
print(fix_spaces(" Example   3"))    # Output: "_Example-3"