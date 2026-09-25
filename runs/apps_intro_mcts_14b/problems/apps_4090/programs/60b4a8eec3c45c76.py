import sys
from collections import defaultdict

def min_length_after_abbreviation(n, words):
    # Create a dictionary to store the start indices of each segment
    segment_indices = defaultdict(list)
    
    # Iterate over the words to find all segments
    for i in range(n):
        for j in range(i + 1, n + 1):
            segment = tuple(words[i:j])
            segment_indices[segment].append((i, j))
    
    # Initialize the minimum length to the original length of the text
    min_length = n * 2  # Each word contributes 2 characters (1 letter + 1 space)
    
    # Check all pairs of non-overlapping equal segments
    for segment, indices in segment_indices.items():
        if len(indices) < 2:
            continue
        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                start1, end1 = indices[i]
                start2, end2 = indices[j]
                if end1 <= start2 or end2 <= start1:
                    # Calculate the new length if we abbreviate these segments
                    new_length = (start1 * 2) + len(segment) + ((end2 - start2) * 2) + (n - end2) * 2
                    min_length = min(min_length, new_length)
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the minimum length after at most one abbreviation
print(min_length_after_abbreviation(n, words))