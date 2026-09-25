def is_palindrome(text: str) -> bool:
    """
    Checks if given string is a palindrome
    >>> is_palindrome('')
    True
    >>> is_palindrome('aba')
    True
    >>> is_palindrome('aaaaa')
    True
    >>> is_palindrome('zbcd')
    False
    """
    # Convert the text to lowercase to ensure case-insensitivity
    text = text.lower()
    
    # Check if the text is equal to its reverse
    return text == text[::-1]