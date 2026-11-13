def minimum_cost_to_complete_tasks():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A = list(map(int, data.split()))
    
    # Sort the tasks by their values
    A.sort()
    
    # Calculate the minimum cost by summing the differences between consecutive elements
    total_cost = sum(abs(A[i] - A[i - 1]) for i in range(1, len(A)))
    
    # Print the result
    print(total_cost)

# Call the function
minimum_cost_to_complete_tasks()