import sys
from collections import Counter

def max_rectangle_area(N, A):
    # Count the frequency of each stick length
    freq = Counter(A)
    
    # Sort the unique stick lengths in descending order
    lengths = sorted(freq.keys(), reverse=True)
    
    max_area = 0
    
    # Iterate over all pairs of stick lengths
    for i in range(len(lengths)):
        for j in range(i + 1, len(lengths)):
            # Check if we have at least two sticks of each length
            if freq[lengths[i]] >= 2 and freq[lengths[j]] >= 2:
                # Calculate the area of the rectangle
                area = lengths[i] * lengths[j]
                # Update the maximum area found
                max_area = max(max_area, area)
    
    return max_area

# Read input from standard input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:]))

# Print the result
print(max_rectangle_area(N, A))