import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        print(-1)
        return

    # We need to find:
    # 1. The first occurrence of '['
    # 2. The last occurrence of ']'
    # 3. Between them, the first occurrence of ':' (after '[')
    # 4. Between them, the last occurrence of ':' (before ']')
    # 5. Between the two colons, count the number of '|'

    n = len(s)
    
    # Find first '['
    first_open = -1
    for i in range(n):
        if s[i] == '[':
            first_open = i
            break
    
    if first_open == -1:
        print(-1)
        return

    # Find last ']'
    last_close = -1
    for i in range(n-1, -1, -1):
        if s[i] == ']':
            last_close = i
            break
    
    if last_close == -1:
        print(-1)
        return

    # Check if '[' comes before ']'
    if first_open >= last_close:
        print(-1)
        return

    # Find first ':' after first_open
    first_colon = -1
    for i in range(first_open + 1, last_close):
        if s[i] == ':':
            first_colon = i
            break
    
    if first_colon == -1:
        print(-1)
        return

    # Find last ':' before last_close
    last_colon = -1
    for i in range(last_close - 1, first_open, -1):
        if s[i] == ':':
            last_colon = i
            break
    
    if last_colon == -1:
        print(-1)
        return

    # Check if first_colon comes before last_colon
    if first_colon >= last_colon:
        print(-1)
        return

    # Count '|' between first_colon and last_colon
    pipe_count = 0
    for i in range(first_colon + 1, last_colon):
        if s[i] == '|':
            pipe_count += 1

    # Length is 4 (for [::]) + pipe_count
    print(4 + pipe_count)

if __name__ == "__main__":
    solve()