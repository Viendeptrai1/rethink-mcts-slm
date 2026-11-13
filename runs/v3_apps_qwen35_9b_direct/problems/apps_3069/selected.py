import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    
    # Check if already valid
    if is_valid(s):
        print("possible")
        return

    # Try all possible segments [l, r] (0-based)
    for l in range(n):
        for r in range(l, n):
            # Create new string with inverted segment
            new_s = list(s)
            for i in range(l, r + 1):
                if new_s[i] == '(':
                    new_s[i] = ')'
                else:
                    new_s[i] = '('
            
            if is_valid("".join(new_s)):
                print("possible")
                return

    print("impossible")

def is_valid(s):
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

if __name__ == "__main__":
    solve()