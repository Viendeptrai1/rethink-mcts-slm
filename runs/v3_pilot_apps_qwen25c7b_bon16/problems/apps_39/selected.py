def max_non_palindrome_substring(s):
    n = len(s)
    max_length = 0
    
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if not is_palindrome(substring):
                max_length = max(max_length, len(substring))
    
    return max_length

# Example usage:
if __name__ == "__main__":
    import sys
    input_string = sys.stdin.read().strip()
    result = max_non_palindrome_substring(input_string)
    print(result)