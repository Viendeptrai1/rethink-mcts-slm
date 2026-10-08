import sys
from typing import List

def main():
    import sys
    import math
    
    def read_int():
        return int(sys.stdin.readline().strip())
    
    def read_floats():
        return list(map(float, sys.stdin.readline().strip().split()))
    
    n = read_int()
    p = read_floats()
    
    # Initialize dp table
    dp = [[0.0] * 2 for _ in range(n + 1)]
    dp[0][0] = 1.0  # Probability of getting 0 problems with 0 friends is 1
    
    for i in range(1, n + 1):
        for j in range(2):
            dp[i][j] = dp[i-1][j] * (1 - p[i-1])  # Friend i does not contribute
            if j == 1:
                dp[i][j] += dp[i-1][j-1] * p[i-1]  # Friend i contributes
    
    result = dp[n][1]
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()