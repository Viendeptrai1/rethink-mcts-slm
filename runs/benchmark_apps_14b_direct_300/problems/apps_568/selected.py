MOD = 10**9 + 7

def count_ways(n):
    total_ways = pow(3, 3 * n, MOD)
    
    valid_ways = 0
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if a + b + c != 6:
                    valid_ways += 1
    
    valid_ways = pow(valid_ways, n, MOD)
    
    return (total_ways - valid_ways) % MOD

if __name__ == "__main__":
    import sys
    n = int(sys.stdin.read().strip())
    print(count_ways(n))