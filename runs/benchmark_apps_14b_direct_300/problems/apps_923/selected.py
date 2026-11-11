import sys

def is_real_puzzle(n, active_teeth):
    # Check if the active_teeth list can be transformed into a sequence 0, 1, ..., n-1
    # by simulating the button presses.
    
    # Create a list to track the direction of rotation for each gear
    directions = [1] * n  # 1 for clockwise, -1 for counter-clockwise
    
    # Simulate the button presses
    for _ in range(n):
        new_active_teeth = []
        for i in range(n):
            # Calculate the new active tooth based on the current direction
            new_active_tooth = (active_teeth[i] + directions[i]) % n
            new_active_teeth.append(new_active_tooth)
        
        # Check if we have reached the desired sequence
        if new_active_teeth == list(range(n)):
            return "Yes"
        
        # Update the directions for the next iteration
        for i in range(n):
            directions[i] *= -1  # Toggle the direction for the next gear
    
    return "No"

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
active_teeth = list(map(int, data[1:]))

# Determine if the puzzle is real
result = is_real_puzzle(n, active_teeth)

# Print the result
print(result)