def is_palindrome(s):
    return s == s[::-1]

def max_non_palindrome_substring_length(s):
    n = len(s)
    max_length = 0
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if not is_palindrome(substring):
                max_length = max(max_length, len(substring))
    
    return max_length

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = max_non_palindrome_substring_length(input)
    print(result)