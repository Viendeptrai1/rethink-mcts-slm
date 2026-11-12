def is_palindrome(s):
    return s == s[::-1]

def max_non_palindrome_length(s):
    n = len(s)
    max_len = 0
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if not is_palindrome(substring):
                max_len = max(max_len, len(substring))
    
    return max_len

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = max_non_palindrome_length(input)
    print(result)