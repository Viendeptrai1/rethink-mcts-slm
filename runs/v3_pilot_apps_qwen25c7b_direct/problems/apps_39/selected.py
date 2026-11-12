def max_non_palindrome_substring(s):
    n = len(s)
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    max_length = 0
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if not is_palindrome(substring):
                max_length = max(max_length, len(substring))
                
    return max_length

# Example usage:
# print(max_non_palindrome_substring("mew"))       # Output: 3
# print(max_non_palindrome_substring("wuffuw"))    # Output: 5
# print(max_non_palindrome_substring("qqqqqqqq"))  # Output: 0