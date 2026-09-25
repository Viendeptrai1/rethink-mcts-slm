import sys
from collections import defaultdict

def min_length_after_abbreviation(n, words):
    # Create a dictionary to store the starting indices of each segment
    segment_indices = defaultdict(list)
    
    # Iterate over all possible segment lengths
    for length in range(2, n + 1):
        # Iterate over all possible starting points for the segment
        for start in range(n - length + 1):
            # Extract the segment
            segment = tuple(words[start:start + length])
            # Store the starting index of this segment
            segment_indices[segment].append(start)
    
    # Initialize the minimum length to the original length of the text
    min_length = n * 2  # Each word has at most 2 characters (1 letter + 1 space)
    
    # Check all possible abbreviations
    for segment, starts in segment_indices.items():
        if len(starts) < 2:
            continue
        # Calculate the length of the abbreviation
        abbreviation_length = len(segment)
        # Calculate the new length of the text if we use this abbreviation
        new_length = 0
        last_end = -1
        for start in starts:
            if start > last_end:
                new_length += (start - last_end - 1) * 2  # Add the length of the words and spaces
            new_length += abbreviation_length  # Add the length of the abbreviation
            last_end = start + len(segment)
        if last_end < n:
            new_length += (n - last_end) * 2  # Add the length of the remaining words and spaces
        # Update the minimum length
        min_length = min(min_length, new_length)
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the result
print(min_length_after_abbreviation(n, words))