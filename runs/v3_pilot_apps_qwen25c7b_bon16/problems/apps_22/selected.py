def check_s_palindrome(s):
    return "TAK" if s == s[::-1][1:] else "NIE"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
result = check_s_palindrome(data[0])
print(result)