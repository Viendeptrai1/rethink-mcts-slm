from typing import List

def max_probability(friends: List[float]) -> float:
    n = len(friends)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for p in friends:
        for j in range(n, 0, -1):
            dp[j] += dp[j-1] * (1-p)
    
    return dp[n]

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    friends = list(map(float, data[1:]))
    
    result = max_probability(friends)
    print(result)