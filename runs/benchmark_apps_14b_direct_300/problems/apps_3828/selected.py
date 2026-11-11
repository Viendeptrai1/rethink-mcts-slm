import sys

def min_actions_to_sort(n, p):
    # Create a list of positions for each car
    positions = [0] * (n + 1)
    for i in range(n):
        positions[p[i]] = i
    
    # Initialize the result with the maximum possible value
    result = n
    
    # Try to calculate the minimum actions needed
    for start in range(n):
        current_position = start
        actions = 0
        visited = [False] * n
        
        for _ in range(n):
            if visited[current_position]:
                break
            visited[current_position] = True
            next_position = positions[current_position + 1]
            actions += abs(next_position - current_position)
            current_position = next_position
        
        result = min(result, actions)
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = list(map(int, data[1:]))

# Calculate and print the result
print(min_actions_to_sort(n, p))