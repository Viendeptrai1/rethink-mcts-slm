def reverse_delete(s, c):
    # Remove all characters in s that are present in c
    result = ''.join(char for char in s if char not in c)
    
    # Check if the result string is a palindrome
    is_palindrome = result == result[::-1]
    
    return (result, is_palindrome)