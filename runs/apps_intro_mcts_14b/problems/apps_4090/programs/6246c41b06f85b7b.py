import sys

def min_length_after_abbreviation(n, words):
    # Calculate the length of the original text
    original_length = sum(len(word) for word in words) + n - 1
    
    # Create a dictionary to store the positions of each word
    word_positions = {}
    for i, word in enumerate(words):
        if word not in word_positions:
            word_positions[word] = []
        word_positions[word].append(i)
    
    # Initialize the minimum length to the original length
    min_length = original_length
    
    # Iterate over each word and its positions
    for word, positions in word_positions.items():
        # If there are less than 2 occurrences of the word, skip it
        if len(positions) < 2:
            continue
        
        # Try to find the longest possible non-overlapping segment
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                start1, end1 = positions[i], positions[i] + len(word) - 1
                start2, end2 = positions[j], positions[j] + len(word) - 1
                
                # Check if the segments are non-overlapping
                if end1 < start2 or end2 < start1:
                    # Calculate the new length after abbreviation
                    new_length = original_length - (len(word) * 2) + 2
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