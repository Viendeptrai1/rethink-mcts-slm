def reverse_delete(s, c):
    # Create a set of characters to delete for O(1) lookup
    delete_chars = set(c)
    
    # Build the result string by keeping only characters not in delete_chars
    result = ''.join(char for char in s if char not in delete_chars)
    
    # Check if the result string is a palindrome
    is_palindrome = result == result[::-1]
    
    return result, is_palindrome