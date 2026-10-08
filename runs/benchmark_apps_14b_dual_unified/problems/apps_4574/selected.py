import sys
from collections import Counter

def max_rectangle_area(N, A):
    # Count occurrences of each stick length
    count = Counter(A)
    
    # Sort the unique lengths in descending order
    lengths = sorted(count.keys(), reverse=True)
    
    max_area = 0
    
    # Iterate over all pairs of lengths
    for i in range(len(lengths)):
        for j in range(i + 1, len(lengths)):
            # Check if we have at least two sticks of each length
            if count[lengths[i]] >= 2 and count[lengths[j]] >= 2:
                # Calculate the area of the rectangle
                area = lengths[i] * lengths[j]
                # Update the maximum area found
                max_area = max(max_area, area)
    
    return max_area

# Read input from stdin
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:]))

# Print the result
print(max_rectangle_area(N, A))