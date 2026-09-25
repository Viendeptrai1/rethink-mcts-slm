import sys
from collections import defaultdict

def min_length_after_abbreviation(n, words):
    # Create a dictionary to store the positions of each word
    word_positions = defaultdict(list)
    for i, word in enumerate(words):
        word_positions[word].append(i)
    
    # Function to calculate the length of the text after abbreviation
    def calculate_length(abbreviations):
        new_text = []
        last_index = -1
        for i, word in enumerate(words):
            if i in abbreviations:
                continue
            if last_index == -1 or i != last_index + 1:
                new_text.append(word)
            else:
                new_text[-1] += ' ' + word
            last_index = i
        return len(' '.join(new_text))
    
    # Try to find the best abbreviation
    min_length = float('inf')
    for word, positions in word_positions.items():
        if len(positions) < 2:
            continue
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                segment_length = positions[j] - positions[i] + 1
                abbreviations = set(range(positions[i], positions[i] + segment_length))
                for k in range(j + 1, len(positions)):
                    if positions[k] - positions[k - 1] == segment_length:
                        abbreviations.update(range(positions[k], positions[k] + segment_length))
                new_length = calculate_length(abbreviations)
                min_length = min(min_length, new_length)
    
    # If no abbreviation was found, return the original length
    if min_length == float('inf'):
        min_length = len(' '.join(words))
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the result
result = min_length_after_abbreviation(n, words)
print(result)