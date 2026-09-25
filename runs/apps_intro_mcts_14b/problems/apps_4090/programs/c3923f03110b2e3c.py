import sys

def min_length_after_abbreviation(n, words):
    text = ' '.join(words)
    min_length = len(text)
    
    # Create a dictionary to store the start indices of each segment
    segment_indices = {}
    
    # Iterate over all possible segment lengths
    for length in range(2, n + 1):
        # Iterate over all possible starting points for the segment
        for start in range(n - length + 1):
            segment = tuple(words[start:start + length])
            if segment not in segment_indices:
                segment_indices[segment] = []
            segment_indices[segment].append(start)
        
        # Check if there are at least two non-intersecting equal segments
        for segment, starts in segment_indices.items():
            if len(starts) >= 2:
                # Calculate the new length if we replace these segments
                abbreviation_length = len(segment) * 2 - 1  # Length of the abbreviation
                new_length = len(text) - (length - 1) * 2 * len(starts) + abbreviation_length
                min_length = min(min_length, new_length)
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the result
result = min_length_after_abbreviation(n, words)
print(result)