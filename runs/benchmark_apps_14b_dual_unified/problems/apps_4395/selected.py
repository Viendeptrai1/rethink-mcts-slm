import sys

def min_recolorings(n, s):
    # Initialize the count of recolors
    recolors = 0
    
    # Initialize the result string
    result = list(s)
    
    # Iterate over the garland
    for i in range(n):
        # Determine the target color for the current position
        if i % 3 == 0:
            target_color = 'R'
        elif i % 3 == 1:
            target_color = 'G'
        else:
            target_color = 'B'
        
        # If the current lamp is not the target color, recolor it
        if s[i] != target_color:
            result[i] = target_color
            recolors += 1
    
    return recolors, ''.join(result)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Get the result
r, t = min_recolorings(n, s)

# Print the result
print(r)
print(t)