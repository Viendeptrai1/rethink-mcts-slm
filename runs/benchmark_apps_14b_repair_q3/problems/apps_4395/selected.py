def make_garland_nice(n, s):
    # Initialize the minimum recolor count to a large number
    min_recolors = float('inf')
    best_garland = ""
    
    # Try each color as the starting color for the pattern
    for start_color in ['R', 'G', 'B']:
        current_recolors = 0
        current_garland = []
        
        # Generate the garland based on the starting color
        for i in range(n):
            if s[i] != start_color:
                current_recolors += 1
            current_garland.append(start_color)
            
            # Update start_color to the next color in the sequence
            if start_color == 'R':
                start_color = 'G'
            elif start_color == 'G':
                start_color = 'B'
            else:
                start_color = 'R'
        
        # Update the best garland if this one has fewer recolors
        if current_recolors < min_recolors:
            min_recolors = current_recolors
            best_garland = ''.join(current_garland)
    
    return min_recolors, best_garland

# Read input
n = int(input())
s = input().strip()

# Get the result
r, t = make_garland_nice(n, s)

# Print the result
print(r)
print(t)