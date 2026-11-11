import sys

def min_actions_to_sort(n, p):
    # Create a list of tuples where each tuple is (car_number, position)
    cars = [(p[i], i) for i in range(n)]
    
    # Sort the cars based on their car numbers
    sorted_cars = sorted(cars)
    
    # Initialize the result with the maximum possible value
    result = n
    
    # Try to find the minimum number of moves by considering two scenarios:
    # 1. Moving cars to the beginning
    # 2. Moving cars to the end
    
    # Scenario 1: Move cars to the beginning
    current_position = 0
    moves = 0
    for i in range(n):
        if sorted_cars[i][1] < current_position:
            moves += 1
        else:
            current_position = sorted_cars[i][1]
    result = min(result, moves)
    
    # Scenario 2: Move cars to the end
    current_position = n - 1
    moves = 0
    for i in range(n):
        if sorted_cars[i][1] > current_position:
            moves += 1
        else:
            current_position = sorted_cars[i][1]
    result = min(result, moves)
    
    return result

# Read input
n = int(sys.stdin.readline().strip())
p = list(map(int, sys.stdin.readline().strip().split()))

# Print the result
print(min_actions_to_sort(n, p))