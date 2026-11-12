def check_s_palindrome(s):
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return "TAK" if s[:mid] == s[mid:][::-1] else "NIE"
    else:
        return "TAK" if s[:mid] == s[mid+1:][::-1] else "NIE"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(check_s_palindrome(input))