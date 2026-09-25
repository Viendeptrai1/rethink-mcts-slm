import sys

def min_text_length_after_abbreviation(n, words):
    # Create a dictionary to store the positions of each segment
    segment_positions = {}
    
    # Iterate over all possible segment lengths
    for length in range(2, n + 1):
        # Iterate over all possible starting positions for the segment
        for start in range(n - length + 1):
            # Extract the segment
            segment = tuple(words[start:start + length])
            # If the segment is already in the dictionary, check for non-intersecting segments
            if segment in segment_positions:
                for prev_start in segment_positions[segment]:
                    # Calculate the end positions of the current and previous segments
                    current_end = start + length - 1
                    prev_end = prev_start + length - 1
                    # Check if the segments are non-intersecting
                    if current_end < prev_start or prev_end < start:
                        # Calculate the new length of the text after abbreviation
                        new_length = len(' '.join(words[:start])) + 1 + length + 1 + len(' '.join(words[current_end + 1:]))
                        return new_length
            # Add the current segment to the dictionary
            if segment not in segment_positions:
                segment_positions[segment] = []
            segment_positions[segment].append(start)
    
    # If no abbreviation is possible, return the original length of the text
    return len(' '.join(words))

# Read input from standard input
input = sys.stdin.read().split()
n = int(input[0])
words = input[1:]

# Calculate and print the minimum length of the text after at most one abbreviation
print(min_text_length_after_abbreviation(n, words))