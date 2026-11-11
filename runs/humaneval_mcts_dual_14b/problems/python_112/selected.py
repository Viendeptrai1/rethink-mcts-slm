def reverse_delete(s, c):
    # Create a set of characters to delete for faster lookup
    delete_set = set(c)
    
    # Construct the result string by excluding characters found in c
    result = ''.join(char for char in s if char not in delete_set)
    
    # Check if the result string is a palindrome
    is_palindrome = result == result[::-1]
    
    # Return the result string and the palindrome check result
    return (result, is_palindrome)