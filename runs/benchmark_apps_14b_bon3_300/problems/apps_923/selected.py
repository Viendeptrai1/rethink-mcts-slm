import sys

def is_real_puzzle(n, active_teeth):
    # Check if the sequence can be transformed into 0, 1, 2, ..., n-1
    target_sequence = list(range(n))
    
    # Try to match the target sequence by rotating the gears
    for _ in range(n):
        if active_teeth == target_sequence:
            return "Yes"
        
        # Rotate the gears
        next_active_teeth = [0] * n
        for i in range(n):
            if i % 2 == 0:
                # Clockwise rotation
                next_active_teeth[i] = (active_teeth[i] + 1) % n
            else:
                # Counter-clockwise rotation
                next_active_teeth[i] = (active_teeth[i] - 1) % n
        
        active_teeth = next_active_teeth
    
    return "No"

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
active_teeth = list(map(int, data[1:]))

# Determine if the puzzle is real
result = is_real_puzzle(n, active_teeth)
print(result)