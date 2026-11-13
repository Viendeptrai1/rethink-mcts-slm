def max_skill_sum(n, a, b):
    # Function to check if a student x can think that they are better than student y
    def is_better(x, y):
        return (a[x] & a[y]) != a[x]

    # Initialize the maximum sum to 0
    max_sum = 0

    # Iterate over all pairs of students
    for i in range(n):
        for j in range(i + 1, n):
            # Check if the pair (i, j) can work together calmly
            if not is_better(i, j) and not is_better(j, i):
                # Calculate the sum of skill levels for this pair
                current_sum = b[i] + b[j]
                # Update the maximum sum if the current sum is greater
                max_sum = max(max_sum, current_sum)

    return max_sum

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:n+1]))
b = list(map(int, data[n+1:2*n+1]))

# Output the result
print(max_skill_sum(n, a, b))