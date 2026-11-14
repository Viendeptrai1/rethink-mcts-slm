import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    symmetric_chars = set("AHIMOTUVWXY")
    
    # Check if all characters are symmetric
    for char in s:
        if char not in symmetric_chars:
            print("NO")
            return
    
    # Check if the string is a palindrome
    if s == s[::-1]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()