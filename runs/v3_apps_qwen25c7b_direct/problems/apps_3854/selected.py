from typing import List

def find_possible_values(n: int, k: int, coins: List[int]) -> List[int]:
    possible = [False] * (k + 1)
    possible[0] = True
    
    for coin in coins:
        for j in range(k, coin - 1, -1):
            if possible[j - coin]:
                possible[j] = True
                
    result = []
    for i in range(k + 1):
        if possible[i]:
            result.append(i)
    
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
coins = list(map(int, data[2:]))

# Find and print the results
result = find_possible_values(n, k, coins)
print(len(result))
print(" ".join(map(str, result)))