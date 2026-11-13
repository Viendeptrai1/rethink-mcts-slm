import sys

def min_distance(N, K, x):
    # Calculate the distance for type-A robots
    dist_A = sum(abs(x[i] - i) * 2 for i in range(N))
    
    # Calculate the distance for type-B robots
    dist_B = sum(abs(K - x[i] + i) * 2 for i in range(N))
    
    return min(dist_A, dist_B)

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
x = list(map(int, data[2:]))

# Print the result
print(min_distance(N, K, x))