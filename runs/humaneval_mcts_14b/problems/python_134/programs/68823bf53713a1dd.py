def check_if_last_char_is_a_letter(txt):
    '''
    Create a function that returns True if the last character
    of a given string is an alphabetical character and is not
    a part of a word, and False otherwise.
    Note: "word" is a group of characters separated by space.

    Examples:
    check_if_last_char_is_a_letter("apple pie") ➞ False
    check_if_last_char_is_a_letter("apple pi e") ➞ True
    check_if_last_char_is_a_letter("apple pi e ") ➞ False
    check_if_last_char_is_a_letter("") ➞ False 
    '''
    # Step 1: Check if the input string is empty
    if not txt:
        return False
    
    # Step 2: Strip any trailing whitespace from the string
    txt = txt.rstrip()
    
    # Step 3: Split the string into words
    words = txt.split()
    
    # Step 4: Check if the last character of the last word is an alphabetical character
    if words and words[-1].isalpha():
        return True
    
    return False