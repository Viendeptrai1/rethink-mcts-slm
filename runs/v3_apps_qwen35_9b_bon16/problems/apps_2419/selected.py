import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        a = int(next(iterator))
        b = int(next(iterator))
        
        if a == b:
            results.append(0)
            continue
        
        diff = abs(a - b)
        
        # Find the smallest n such that sum(1..n) >= diff
        # sum = n*(n+1)/2 >= diff
        # n^2 + n - 2*diff >= 0
        # Roots: (-1 + sqrt(1 + 8*diff)) / 2
        n = int(math.ceil((-1 + math.sqrt(1 + 8 * diff)) / 2))
        
        current_sum = n * (n + 1) // 2
        parity = (current_sum - diff) % 2
        
        # If parity is even, we can distribute the extra sum to keep equality
        # If parity is odd, we need one more operation to flip parity
        if parity == 0:
            results.append(n)
        else:
            results.append(n + 1)
    
    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()