import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    results = []
    for _ in range(t):
        a = int(data[idx])
        b = int(data[idx+1])
        x = int(data[idx+2])
        y = int(data[idx+3])
        n = int(data[idx+4])
        idx += 5
        
        ans = float('inf')
        
        # Strategy 1: Reduce a as much as possible first
        reduce_a = min(n, a - x)
        new_a = a - reduce_a
        new_n = n - reduce_a
        reduce_b = min(new_n, b - y)
        new_b = b - reduce_b
        ans = min(ans, new_a * new_b)
        
        # Strategy 2: Reduce b as much as possible first
        reduce_b = min(n, b - y)
        new_b = b - reduce_b
        new_n = n - reduce_b
        reduce_a = min(new_n, a - x)
        new_a = a - reduce_a
        ans = min(ans, new_a * new_b)
        
        results.append(str(ans))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == "__main__":
    solve()