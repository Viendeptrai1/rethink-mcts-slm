import sys
from collections import defaultdict

def min_length_after_abbreviation(n, words):
    # Create a dictionary to store the start indices of each segment
    segment_indices = defaultdict(list)
    
    # Iterate over all possible segment lengths
    for length in range(1, n // 2 + 1):
        # Iterate over all possible starting points for the first segment
        for start1 in range(n - length + 1):
            # Get the first segment
            segment1 = tuple(words[start1:start1 + length])
            # Store the start index of the first segment
            segment_indices[segment1].append(start1)
    
    # Initialize the minimum length to the original length of the text
    min_length = n
    
    # Iterate over all segments in the dictionary
    for segment, starts in segment_indices.items():
        # If there is more than one occurrence of the segment
        if len(starts) > 1:
            # Calculate the length of the abbreviation
            abbreviation_length = len(segment)
            # Iterate over all pairs of start indices
            for i in range(len(starts)):
                for j in range(i + 1, len(starts)):
                    start1, start2 = starts[i], starts[j]
                    # Calculate the new length of the text after abbreviation
                    new_length = n - 2 * length + abbreviation_length
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