import sys

def min_actions_to_sort(n, p):
    # Create a list of tuples (value, index) and sort it by value
    sorted_positions = sorted((value, idx) for idx, value in enumerate(p))
    
    # Initialize the result with the length of the list
    result = n
    
    # Iterate over each possible starting point
    for start in range(n):
        # Calculate the number of inversions if we start from this point
        inversions = 0
        for i in range(n):
            current_pos = (start + i) % n
            next_pos = (start + i + 1) % n
            if sorted_positions[current_pos][1] > sorted_positions[next_pos][1]:
                inversions += 1
        
        # Update the result with the minimum inversions found
        result = min(result, inversions)
    
    return result

# Read input
n = int(sys.stdin.readline())
p = list(map(int, sys.stdin.readline().split()))

# Print the result
print(min_actions_to_sort(n, p))