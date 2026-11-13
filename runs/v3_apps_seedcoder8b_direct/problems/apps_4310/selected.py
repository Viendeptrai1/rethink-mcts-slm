def min_cost_to_complete_tasks():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A = list(map(int, data.split()))
    
    # Sort the tasks by their values
    A.sort()
    
    # The minimum cost to complete all tasks
    # Start with the first task at cost 0
    # Then move to the last task, which is the farthest from the first
    min_cost = abs(A[2] - A[0])
    
    print(min_cost)