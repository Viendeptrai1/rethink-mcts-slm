def max_skill_sum(n, a, b):
    # Function to check if student x can think that student y is better
    def can_x_think_better_than_y(x, y):
        return (a[x] & a[y]) != a[x]

    # Initialize the maximum skill sum
    max_sum = 0

    # Iterate over all pairs of students
    for i in range(n):
        for j in range(i + 1, n):
            # Check if the students can work together calmly
            if not (can_x_think_better_than_y(i, j) or can_x_think_better_than_y(j, i)):
                # Calculate the sum of the skill levels of this group
                current_sum = b[i] + b[j]
                # Update the maximum skill sum if needed
                if current_sum > max_sum:
                    max_sum = current_sum

    return max_sum

# Reading input from standard input
import sys
input = sys.stdin.read
data = input().split()

# Parse the input values
n = int(data[0])
a = list(map(int, data[1:n+1]))
b = list(map(int, data[n+1:2*n+1]))

# Get the result and print it
result = max_skill_sum(n, a, b)
print(result)