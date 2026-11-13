import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        x = int(next(iterator))
        
        # The dice has faces 2, 3, 4, 5, 6, 7.
        # Minimum sum for k rolls = 2 * k
        # Maximum sum for k rolls = 7 * k
        # We need to find a k such that: 2*k <= x <= 7*k
        # This is equivalent to: k >= x/7 and k <= x/2
        # Since we need the smallest integer k that satisfies k >= x/7,
        # we can simply calculate ceil(x / 7).
        # Let's verify: if k = ceil(x/7), then 7*k >= x.
        # Also, since k = ceil(x/7) <= x/2 (because x >= 2, x/7 <= x/2),
        # then 2*k <= x holds as well.
        
        # Calculate ceil(x / 7) using integer arithmetic: (x + 6) // 7
        k = (x + 6) // 7
        results.append(str(k))
    
    print('\n'.join(results))

if __name__ == "__main__":
    solve()