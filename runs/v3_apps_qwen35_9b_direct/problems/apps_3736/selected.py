import sys

def solve():
    s = sys.stdin.readline().strip()
    mirror_chars = set(['A', 'H', 'I', 'M', 'O', 'T', 'U', 'V', 'W', 'X', 'Y'])
    
    # Check if all characters are mirror-symmetric
    for char in s:
        if char not in mirror_chars:
            print("NO")
            return
    
    # Check if the string is a palindrome
    if s == s[::-1]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()