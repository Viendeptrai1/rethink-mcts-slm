import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[i+1]))
    
    res = [0] * n
    
    last_inc = -1
    last_dec = float('inf')
    
    possible = True
    
    for i in range(n):
        val = a[i]
        assigned = False
        
        # Try to assign to increasing sequence
        if val > last_inc:
            res[i] = 0
            last_inc = val
            assigned = True
        # Try to assign to decreasing sequence
        elif val < last_dec:
            res[i] = 1
            last_dec = val
            assigned = True
        
        if not assigned:
            possible = False
            break
    
    if possible:
        print("YES")
        print(*(res))
    else:
        print("NO")

if __name__ == "__main__":
    solve()