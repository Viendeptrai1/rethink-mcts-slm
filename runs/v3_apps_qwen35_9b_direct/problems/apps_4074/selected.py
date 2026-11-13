import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        n = int(next(iterator))
        k = int(next(iterator))
        
        # We need to find the smallest x such that n % x == 0 and 1 <= x <= k.
        # If such an x exists, the number of packages is n // x.
        # To minimize n // x, we need to maximize x.
        # The largest divisor of n that is <= k is the answer.
        
        # Strategy:
        # 1. If k >= n, then we can choose x = n (since n is a divisor of n and n <= k).
        #    Then packages = n // n = 1.
        # 2. If k < n, we need the largest divisor of n that is <= k.
        #    We can iterate from 1 up to sqrt(n). For each divisor d of n:
        #       - If d <= k, then d is a candidate.
        #       - If n // d <= k, then n // d is a candidate (and it's larger than d usually).
        #    We track the maximum candidate found.
        
        if k >= n:
            results.append(1)
        else:
            best_x = 1
            limit = int(n**0.5)
            for i in range(1, limit + 1):
                if n % i == 0:
                    d1 = i
                    d2 = n // i
                    
                    if d1 <= k:
                        if d1 > best_x:
                            best_x = d1
                    if d2 <= k:
                        if d2 > best_x:
                            best_x = d2
            
            results.append(n // best_x)
    
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()