import sys

def min_distance(N, K, x):
    total_distance = 0
    for xi in x:
        distance_to_ball_A = abs(0 - xi)
        distance_back_to_original_A = abs(xi - 0)
        distance_to_ball_B = abs(K - xi)
        distance_back_to_original_B = abs(xi - K)
        total_distance += min(distance_to_ball_A + distance_back_to_original_A,
                              distance_to_ball_B + distance_back_to_original_B)
    return total_distance

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
x = list(map(int, data[2:]))

# Calculate and print the result
print(min_distance(N, K, x))