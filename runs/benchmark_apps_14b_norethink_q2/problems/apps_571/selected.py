import sys

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    balance = 0
    result = []
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        elif s[i] == ')':
            balance -= 1
        else:  # s[i] == '?'
            if balance < 0:
                result.append('(')
                balance += 1
            else:
                result.append(')')
                balance -= 1
        
        if balance < 0:
            return ":("
    
    if balance != 0:
        return ":("
    
    return ''.join(result)

if __name__ == "__main__":
    print(solve())