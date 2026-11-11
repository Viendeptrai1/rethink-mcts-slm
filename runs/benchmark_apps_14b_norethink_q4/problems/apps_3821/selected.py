import sys
from typing import List

def max_probability(n: int, p: List[float]) -> float:
    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    
    for prob in p:
        new_dp = [0.0] * (n + 1)
        for i in range(n + 1):
            if i > 0:
                new_dp[i] += dp[i - 1] * prob
            if i < n:
                new_dp[i] += dp[i] * (1 - prob)
        dp = new_dp
    
    return dp[1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = list(map(float, data[1:]))
    
    result = max_probability(n, p)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()