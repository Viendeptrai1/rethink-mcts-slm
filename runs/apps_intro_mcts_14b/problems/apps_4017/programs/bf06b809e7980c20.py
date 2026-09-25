import sys

def find_nice_indices(n, a):
    total_sum = sum(a)
    prefix_sum = 0
    nice_indices = []

    for i in range(n):
        # Calculate the left sum and right sum
        left_sum = prefix_sum
        right_sum = total_sum - prefix_sum - a[i]
        
        # Check if the current element is equal to the sum of the remaining elements
        if a[i] == left_sum + right_sum:
            nice_indices.append(i + 1)
        
        # Update the prefix sum
        prefix_sum += a[i]

    # Print the result
    print(len(nice_indices))
    if nice_indices:
        print(" ".join(map(str, nice_indices)))

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Find and print nice indices
find_nice_indices(n, a)