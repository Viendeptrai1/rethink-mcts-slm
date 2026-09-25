import sys

def is_palindrome(a):
    return str(a) == str(a)[::-1]

if __name__ == "__main__":
    a = int(sys.stdin.read().strip())
    result = 1 if is_palindrome(a) else 0
    print(result)