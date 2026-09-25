def check_if_last_char_is_a_letter(txt):
    # Strip any trailing whitespace from the text
    txt = txt.rstrip()
    
    # Check if the text is empty after stripping
    if not txt:
        return False
    
    # Split the text into words
    words = txt.split()
    
    # Get the last word
    last_word = words[-1]
    
    # Check if the last word is a single letter
    if len(last_word) == 1 and last_word.isalpha():
        return True
    
    return False

# Test cases
print(check_if_last_char_is_a_letter("apple pie"))  # ➞ False
print(check_if_last_char_is_a_letter("apple pi e"))  # ➞ True
print(check_if_last_char_is_a_letter("apple pi e "))  # ➞ False
print(check_if_last_char_is_a_letter(""))  # ➞ False