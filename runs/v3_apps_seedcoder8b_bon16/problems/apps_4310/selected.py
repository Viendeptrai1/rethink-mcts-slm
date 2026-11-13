def min_cost_to_complete_tasks():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A = list(map(int, data.split()))
    
    # Sort the array to minimize cost
    A.sort()
    
    # The cost to complete tasks is the minimum of:
    # - Completing in order: A[0] -> A[1] -> A[2]
    # - Completing in order: A[2] -> A[1] -> A[0]
    cost1 = abs(A[1] - A[0]) + abs(A[2] - A[1])
    cost2 = abs(A[2] - A[0]) + abs(A[1] - A[2])
    
    # The minimum cost will be the minimum of the two possible costs
    print(min(cost1, cost2))

# This function should be called when the script is run
min_cost_to_complete_tasks()