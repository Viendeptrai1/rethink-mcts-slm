import sys

def solve():
    n = int(input())
    s = input()
    
    open_count = 0
    result = []
    
    for i in range(n):
        if s[i] == '(':
            open_count += 1
            result.append('(')
        elif s[i] == ')':
            if open_count == 0:
                print(":(")
                return
            open_count -= 1
            result.append(')')
        else:  # s[i] == '?'
            if open_count > 0:
                open_count -= 1
                result.append(')')
            else:
                result.append('(')
                open_count += 1
    
    # Check if all open parentheses are closed
    if open_count > 0:
        print(":(")
        return
    
    print(''.join(result))

if __name__ == "__main__":
    solve()