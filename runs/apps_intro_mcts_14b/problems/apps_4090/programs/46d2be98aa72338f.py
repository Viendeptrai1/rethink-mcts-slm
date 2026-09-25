import sys

def min_length_after_abbreviation(n, words):
    # Calculate the original length of the text
    original_length = sum(len(word) for word in words) + n - 1
    
    # Find all equal segments
    segments = {}
    for i in range(n):
        for j in range(i + 1, n):
            segment = tuple(words[i:j+1])
            if segment not in segments:
                segments[segment] = []
            segments[segment].append((i, j))
    
    # Initialize the minimum length to the original length
    min_length = original_length
    
    # Check each segment for possible abbreviations
    for segment, positions in segments.items():
        if len(positions) < 2:
            continue
        # Calculate the abbreviation length
        abbreviation_length = len(segment) * 2
        # Calculate the new length if we replace all occurrences of this segment
        new_length = original_length
        for start, end in positions:
            new_length -= (end - start + 1) * 2
            new_length += abbreviation_length
        # Update the minimum length
        min_length = min(min_length, new_length)
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Output the result
print(min_length_after_abbreviation(n, words))