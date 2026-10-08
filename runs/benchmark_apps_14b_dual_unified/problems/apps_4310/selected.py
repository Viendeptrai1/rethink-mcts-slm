import sys

def min_cost_to_complete_tasks(A):
    # Calculate the cost for each possible order of completing the tasks
    cost1 = 0 + abs(A[1] - A[0]) + abs(A[2] - A[1])
    cost2 = 0 + abs(A[0] - A[1]) + abs(A[2] - A[0])
    cost3 = 0 + abs(A[1] - A[2]) + abs(A[0] - A[1])
    cost4 = 0 + abs(A[2] - A[1]) + abs(A[0] - A[2])
    cost5 = 0 + abs(A[0] - A[2]) + abs(A[1] - A[0])
    cost6 = 0 + abs(A[2] - A[0]) + abs(A[1] - A[2])
    
    # Return the minimum cost among all possible orders
    return min(cost1, cost2, cost3, cost4, cost5, cost6)

# Read input from standard input
input = sys.stdin.read
data = input().split()
A = list(map(int, data))

# Print the result
print(min_cost_to_complete_tasks(A))