import sys

def max_score(N, a):
    prefix_sum = [0] * (3*N + 1)
    for i in range(1, 3*N + 1):
        prefix_sum[i] = prefix_sum[i-1] + a[i-1]
    
    max_score = float('-inf')
    for i in range(N, 2*N):
        left_half = prefix_sum[2*N] - prefix_sum[i+1]
        right_half = prefix_sum[i] - prefix_sum[N]
        current_score = left_half - right_half
        if current_score > max_score:
            max_score = current_score
    
    return max_score

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

# Print the result
print(max_score(N, a))