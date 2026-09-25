import sys
from typing import List

def min_days_to_finish_coursework(n: int, m: int, a: List[int]) -> int:
    # Sort the coffee cups by caffeine content in descending order
    a.sort(reverse=True)
    
    # Initialize a DP table where dp[i] represents the minimum number of days needed to write i pages
    dp = [float('inf')] * (m + 1)
    dp[0] = 0
    
    # Iterate over each possible number of days
    for days in range(1, n + 1):
        # Update the DP table for the current number of days
        for pages_written in range(m, -1, -1):
            for i in range(days):
                if pages_written + max(0, a[i] - i) <= m:
                    dp[pages_written + max(0, a[i] - i)] = min(dp[pages_written + max(0, a[i] - i)], days)
    
    # Find the minimum number of days needed to write at least m pages
    result = float('inf')
    for pages_written in range(m, -1, -1):
        result = min(result, dp[pages_written])
    
    return result if result != float('inf') else -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    result = min_days_to_finish_coursework(n, m, a)
    print(result)

if __name__ == "__main__":
    main()