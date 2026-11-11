def can_hit_all_targets_with_two_shots(N, targets):
    from collections import defaultdict
    
    # Dictionary to store the count of each unique slope
    slope_count = defaultdict(int)
    
    # Calculate slopes for each pair of targets
    for i in range(N):
        for j in range(i + 1, N):
            x1, y1 = targets[i]
            x2, y2 = targets[j]
            
            if x1 == x2:
                # Infinite slope (vertical line)
                slope = float('inf')
            else:
                # Finite slope
                slope = (y2 - y1) / (x2 - x1)
            
            # Increment the count of this slope
            slope_count[slope] += 1
    
    # Check the number of unique slopes
    unique_slopes = len(slope_count)
    
    # If there are more than 2 unique slopes, it's not possible to hit all targets with 2 shots
    if unique_slopes > 2:
        return "failure"
    else:
        return "success"

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
targets = []
index = 1
for i in range(N):
    x = int(data[index])
    y = int(data[index + 1])
    targets.append((x, y))
    index += 2

# Output the result
print(can_hit_all_targets_with_two_shots(N, targets))