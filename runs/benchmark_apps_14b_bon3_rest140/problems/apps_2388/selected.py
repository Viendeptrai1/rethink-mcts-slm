import sys
from typing import List, Tuple

MOD = 998244353

def count_remaining_robots(N: int, robots: List[Tuple[int, int]]) -> int:
    # Sort robots by their starting position
    robots.sort()
    
    # Initialize DP array
    dp = [0] * (N + 1)
    dp[0] = 1
    
    # Iterate over each robot
    for i in range(N):
        x, d = robots[i]
        # Update DP array in reverse to avoid overwriting
        for j in range(N, i, -1):
            if robots[j-1][0] >= x + d:
                break
            dp[j] = (dp[j] + dp[j-1]) % MOD
    
    # Sum up all possible states where some robots remain
    result = sum(dp[1:]) % MOD
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    robots = []
    index = 1
    for i in range(N):
        x = int(data[index])
        d = int(data[index + 1])
        robots.append((x, d))
        index += 2
    
    result = count_remaining_robots(N, robots)
    print(result)

if __name__ == "__main__":
    main()