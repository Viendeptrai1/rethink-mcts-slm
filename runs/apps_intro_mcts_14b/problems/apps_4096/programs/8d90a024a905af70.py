import sys
from typing import List

def min_days_to_complete_coursework(n: int, m: int, a: List[int]) -> int:
    # Sort the caffeine levels in descending order
    a.sort(reverse=True)
    
    # Initialize the DP table
    dp = [float('inf')] * (m + 1)
    dp[0] = 0
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(n):
            if i >= a[j]:
                dp[i] = min(dp[i], dp[i - a[j]] + 1)
    
    # If dp[m] is still infinity, it means it's impossible to write m pages
    return dp[m] if dp[m] != float('inf') else -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    result = min_days_to_complete_coursework(n, m, a)
    print(result)

if __name__ == "__main__":
    main()