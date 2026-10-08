def max_significance(n, m, d, physics_cups, informatics_cups):
    # Sort cups by significance in descending order
    physics_cups.sort(key=lambda x: -x[0])
    informatics_cups.sort(key=lambda x: -x[0])
    
    # Initialize variables
    max_significance = 0
    current_width = 0
    selected_physics = []
    selected_informatics = []
    
    # Helper function to check if we can add a cup
    def can_add_cup(cup, selected):
        return current_width + cup[1] <= d and len(selected) > 0
    
    # Try to add the most significant cups first
    for c, w in physics_cups:
        if current_width + w <= d:
            selected_physics.append((c, w))
            current_width += w
        else:
            break
    
    for c, w in informatics_cups:
        if current_width + w <= d:
            selected_informatics.append((c, w))
            current_width += w
        else:
            break
    
    # If we have at least one cup from each subject, calculate the significance
    if selected_physics and selected_informatics:
        max_significance = sum(c for c, w in selected_physics) + sum(c for c, w in selected_informatics)
    
    # Backtrack to find the optimal solution
    for i in range(len(selected_physics)):
        for j in range(len(selected_informatics)):
            current_width = sum(w for c, w in selected_physics[:i+1]) + sum(w for c, w in selected_informatics[:j+1])
            if current_width <= d:
                max_significance = max(max_significance, 
                                      sum(c for c, w in selected_physics[:i+1]) + sum(c for c, w in selected_informatics[:j+1]))
    
    return max_significance

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])

physics_cups = []
informatics_cups = []

index = 3
for _ in range(n):
    c = int(data[index])
    w = int(data[index + 1])
    physics_cups.append((c, w))
    index += 2

for _ in range(m):
    c = int(data[index])
    w = int(data[index + 1])
    informatics_cups.append((c, w))
    index += 2

# Calculate and print the result
result = max_significance(n, m, d, physics_cups, informatics_cups)
print(result)