import sys

def max_intersection_length(n, segments):
    # Sort segments by their left endpoint
    segments.sort()
    
    # Initialize variables to track the maximum intersection length
    max_length = 0
    current_left = segments[0][0]
    current_right = segments[0][1]
    
    # Calculate the intersection length if we remove each segment one by one
    for i in range(n):
        # Calculate the intersection length excluding the i-th segment
        if i == 0:
            left = segments[1][0]
            right = min(current_right, segments[1][1])
        elif i == n - 1:
            left = max(current_left, segments[n-2][0])
            right = segments[n-2][1]
        else:
            left = max(current_left, segments[i-1][0])
            right = min(current_right, segments[i+1][1])
        
        # Update the maximum intersection length
        if right >= left:
            max_length = max(max_length, right - left)
        
        # Update current_left and current_right for the next iteration
        if i < n - 1:
            current_left = segments[i+1][0]
            current_right = segments[i+1][1]
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
segments = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]

# Calculate and print the result
result = max_intersection_length(n, segments)
print(result)