import sys

def min_cost_to_complete_tasks(A):
    A.sort()
    return abs(A[0] - A[2])

# Read input from standard input
input_line = sys.stdin.read().strip()
A = list(map(int, input_line.split()))

# Calculate the minimum cost to complete all tasks
min_cost = min_cost_to_complete_tasks(A)

# Print the result
print(min_cost)