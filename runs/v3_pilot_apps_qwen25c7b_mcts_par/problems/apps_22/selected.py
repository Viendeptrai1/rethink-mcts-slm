def check_s_palindrome(s):
    n = len(s)
    for i in range(n // 2):
        if s[i] != s[n - i - 1]:
            return "NIE"
    return "TAK"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = check_s_palindrome(input)
    print(result)