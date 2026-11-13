import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    
    # Find first '['
    first_bracket = -1
    for i in range(n):
        if s[i] == '[':
            first_bracket = i
            break
    if first_bracket == -1:
        print(-1)
        return
    
    # Find first ':' after first '['
    first_colon = -1
    for i in range(first_bracket + 1, n):
        if s[i] == ':':
            first_colon = i
            break
    if first_colon == -1:
        print(-1)
        return
    
    # Find last ':' before last ']'
    last_colon = -1
    last_bracket = -1
    for i in range(n - 1, -1, -1):
        if s[i] == ']':
            last_bracket = i
            break
    if last_bracket == -1:
        print(-1)
        return
    
    for i in range(last_bracket - 1, -1, -1):
        if s[i] == ':':
            last_colon = i
            break
    if last_colon == -1:
        print(-1)
        return
    
    # Check order: [ < first_colon < last_colon < ]
    if first_colon >= last_colon or last_colon >= last_bracket:
        print(-1)
        return
    
    # Count '|' between first_colon and last_colon
    count_pipes = 0
    for i in range(first_colon + 1, last_colon):
        if s[i] == '|':
            count_pipes += 1
    
    # Length is 4 (for [::]) + count of pipes
    print(4 + count_pipes)

if __name__ == "__main__":
    solve()