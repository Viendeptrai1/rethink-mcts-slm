import sys
from math import comb

MOD = 10**9 + 7

def count_ways(n, k):
    if n == 1:
        return k % MOD
    
    total_ways = 0
    for i in range(1, k+1):
        for j in range(1, k+1):
            if i <= j:
                total_ways += comb(k-1, i-1) * comb(k-1, j-1)
                total_ways %= MOD
    
    return total_ways

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    result = count_ways(n, k)
    print(result)