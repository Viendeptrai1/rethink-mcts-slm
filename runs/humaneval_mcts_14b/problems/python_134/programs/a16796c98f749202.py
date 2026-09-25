def check_if_last_char_is_a_letter(txt):
    # Strip any trailing spaces from the text
    txt = txt.rstrip()
    
    # Check if the text is empty after stripping spaces
    if not txt:
        return False
    
    # Check if the last character is an alphabetical character
    if txt[-1].isalpha():
        # Check if the last character is preceded by a space
        if len(txt) == 1 or txt[-2] == ' ':
            return True
    
    return False

# Test cases
print(check_if_last_char_is_a_letter("apple pie"))  # ➞ False
print(check_if_last_char_is_a_letter("apple pi e"))  # ➞ True
print(check_if_last_char_is_a_letter("apple pi e "))  # ➞ False
print(check_if_last_char_is_a_letter(""))  # ➞ False