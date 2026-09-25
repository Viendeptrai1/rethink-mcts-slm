import sys

def min_text_length_after_abbreviation(n, words):
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
    
    # Check all pairs of equal segments
    for segment, positions in segments.items():
        if len(positions) < 2:
            continue
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                start1, end1 = positions[i]
                start2, end2 = positions[j]
                # Ensure segments do not overlap
                if end1 < start2 or end2 < start1:
                    # Calculate the new length if we abbreviate these segments
                    new_length = original_length
                    # Remove the length of the segments
                    new_length -= (end1 - start1 + 1) * 2
                    new_length -= (end2 - start2 + 1) * 2
                    # Add the length of the abbreviations
                    new_length += 2
                    new_length += 2
                    # Update the minimum length
                    min_length = min(min_length, new_length)
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the result
result = min_text_length_after_abbreviation(n, words)
print(result)