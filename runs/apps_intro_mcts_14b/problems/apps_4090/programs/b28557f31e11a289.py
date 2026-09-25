import sys
from collections import defaultdict

def min_length_after_abbreviation(n, words):
    # Create a dictionary to store the starting indices of each segment
    segment_indices = defaultdict(list)
    
    # Iterate over all possible segment lengths
    for length in range(1, n // 2 + 1):
        # Iterate over all possible starting positions for the segment
        for start in range(n - length + 1):
            # Extract the segment
            segment = tuple(words[start:start + length])
            # Store the starting index of the segment
            segment_indices[segment].append(start)
    
    # Initialize the minimum length to the original length of the text
    min_length = n
    
    # Iterate over all segments found
    for segment, starts in segment_indices.items():
        # If there are at least two non-intersecting segments
        if len(starts) >= 2:
            # Calculate the length of the abbreviation
            abbreviation_length = len(segment) * 2
            # Calculate the new length of the text after abbreviation
            new_length = n - (len(starts) - 1) * len(segment) + abbreviation_length
            # Update the minimum length if the new length is smaller
            min_length = min(min_length, new_length)
    
    return min_length

# Read input from standard input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the minimum length after at most one abbreviation
print(min_length_after_abbreviation(n, words))