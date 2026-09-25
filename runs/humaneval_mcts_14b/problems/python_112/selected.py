def reverse_delete(s, c):
    # Step 1: Create a set of characters to delete for faster lookup
    delete_set = set(c)
    
    # Step 2: Build the result string by excluding characters found in delete_set
    result_string = ''.join(char for char in s if char not in delete_set)
    
    # Step 3: Check if the result string is a palindrome
    is_palindrome = result_string == result_string[::-1]
    
    # Step 4: Return the result string and the palindrome check result
    return (result_string, is_palindrome)

# Example usage:
# print(reverse_delete("abcde", "ae"))  # Output: ('bcd', False)
# print(reverse_delete("abcdef", "b"))  # Output: ('acdef', False)
# print(reverse_delete("abcdedcba", "ab"))  # Output: ('cdedc', True)