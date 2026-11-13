def can_hit_all_targets(N, targets):
    # Check if there are less than or equal to 2 targets
    if N <= 2:
        return "success"
    
    # Sort targets by x-coordinate
    targets.sort()
    
    # Try to find two lines that cover all targets
    for i in range(N - 1):
        for j in range(i + 1, N):
            # Extract points
            x1, y1 = targets[i]
            x2, y2 = targets[j]
            
            # Calculate slope and intercept of the line passing through these points
            if x2 == x1:
                # Vertical line
                valid = True
                for k in range(N):
                    if targets[k][0] != x1:
                        valid = False
                        break
                if valid:
                    return "success"
            else:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                
                # Check if all other points lie on this line
                valid = True
                for k in range(N):
                    if k != i and k != j:
                        if targets[k][1] != m * targets[k][0] + c:
                            valid = False
                            break
                if valid:
                    return "success"
    
    return "failure"

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
targets = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Output result
print(can_hit_all_targets(N, targets))