def check_if_last_char_is_a_letter(txt):
    # Step 1: Strip any trailing whitespace from the string
    txt = txt.rstrip()
    
    # Step 2: Check if the string is empty after stripping
    if not txt:
        return False
    
    # Step 3: Split the string into words
    words = txt.split()
    
    # Step 4: Get the last word
    last_word = words[-1]
    
    # Step 5: Check if the last word is a single letter
    return len(last_word) == 1 and last_word.isalpha()

# Test cases
print(check_if_last_char_is_a_letter("apple pie"))  # ➞ False
print(check_if_last_char_is_a_letter("apple pi e"))  # ➞ True
print(check_if_last_char_is_a_letter("apple pi e "))  # ➞ False
print(check_if_last_char_is_a_letter(""))  # ➞ False