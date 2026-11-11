import sys
from typing import List

def largest_k_multiple_free_subset(n: int, k: int, a: List[int]) -> int:
    a.sort()
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if a[i] != a[j] * k:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    result = largest_k_multiple_free_subset(n, k, a)
    print(result)

if __name__ == "__main__":
    main()