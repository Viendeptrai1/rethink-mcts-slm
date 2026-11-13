from typing import List

def find_possible_values(n: int, k: int, coins: List[int]) -> List[int]:
    dp = [False] * (k + 1)
    dp[0] = True
    
    for coin in coins:
        for j in range(k, coin - 1, -1):
            if dp[j - coin]:
                dp[j] = True
    
    possible_values = []
    for i in range(k + 1):
        if dp[i]:
            for j in range(i + 1):
                if dp[j]:
                    possible_values.append(j)
    
    return sorted(set(possible_values))

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    coins = list(map(int, data[2:]))
    
    result = find_possible_values(n, k, coins)
    print(len(result))
    print(" ".join(map(str, result)))