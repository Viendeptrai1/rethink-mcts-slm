import sys

def min_cost_to_complete_tasks(A):
    # Sort the tasks based on their values
    A.sort()
    
    # The minimum cost will be the sum of the differences between consecutive tasks
    return abs(A[1] - A[0]) + abs(A[2] - A[1])

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Convert input strings to integers
A = list(map(int, data))

# Calculate and print the minimum cost
print(min_cost_to_complete_tasks(A))