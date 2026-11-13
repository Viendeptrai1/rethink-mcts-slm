import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
a = list(map(int, data[1:]))

# Calculate prefix sums
prefix_sum = [0] * (3*N + 1)
for i in range(1, 3*N + 1):
    prefix_sum[i] = prefix_sum[i-1] + a[i-1]

# Initialize variables to store the maximum score
max_score = float('-inf')

# Iterate over all possible positions to split the sequence into two halves
for i in range(N, 2*N):
    # Sum of the first half of a'
    first_half_sum = prefix_sum[i+1] - prefix_sum[N]
    # Sum of the second half of a'
    second_half_sum = prefix_sum[3*N] - prefix_sum[i+1]
    # Calculate the score
    score = first_half_sum - second_half_sum
    # Update the maximum score if the current score is higher
    max_score = max(max_score, score)

# Print the maximum possible score
print(max_score)