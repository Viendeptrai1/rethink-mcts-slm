import sys

def max_score(N, a):
    # Split the array into three parts
    left_part = a[:N]
    middle_part = a[N:2*N]
    right_part = a[2*N:]
    
    # Calculate prefix sums for the left part
    prefix_sum_left = [0] * (N + 1)
    for i in range(N):
        prefix_sum_left[i + 1] = prefix_sum_left[i] + left_part[i]
    
    # Calculate suffix sums for the right part
    suffix_sum_right = [0] * (N + 1)
    for i in range(N):
        suffix_sum_right[i] = suffix_sum_right[i + 1] + right_part[N - 1 - i]
    
    # Initialize the maximum score
    max_score = float('-inf')
    
    # Iterate over all possible splits of the middle part
    for i in range(N + 1):
        # Sum of the first half of the resulting sequence
        first_half_sum = prefix_sum_left[i] + sum(middle_part[:i])
        
        # Sum of the second half of the resulting sequence
        second_half_sum = suffix_sum_right[N - i] + sum(middle_part[i:])
        
        # Calculate the score for this split
        score = first_half_sum - second_half_sum
        
        # Update the maximum score
        max_score = max(max_score, score)
    
    return max_score

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

# Print the result
print(max_score(N, a))