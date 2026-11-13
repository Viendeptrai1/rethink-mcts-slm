from math import comb

def count_arrangements(N, K):
    MOD = 10**9 + 7
    result = [0] * (K + 1)
    
    # Calculate the number of ways to arrange the balls
    for i in range(K + 1):
        if i == 0:
            result[i] = 1
        else:
            result[i] = comb(N - 1, i - 1) % MOD
    
    return result[1:]

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])

# Get the result
result = count_arrangements(N, K)

# Print the result
for num in result:
    print(num)