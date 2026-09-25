import sys
from collections import defaultdict

def min_length_after_abbreviation(n, words):
    # Create a dictionary to store the positions of each word
    word_positions = defaultdict(list)
    for i, word in enumerate(words):
        word_positions[word].append(i)
    
    # Function to calculate the length of the text after abbreviation
    def calculate_length(abbreviations):
        total_length = 0
        last_end = -1
        for start, end in sorted(abbreviations):
            if start > last_end:
                total_length += sum(len(words[i]) for i in range(last_end + 1, start))
            total_length += len(words[start])
            last_end = end
        if last_end < n - 1:
            total_length += sum(len(words[i]) for i in range(last_end + 1, n))
        return total_length
    
    # Try to find the best abbreviation
    min_length = float('inf')
    for word, positions in word_positions.items():
        if len(positions) >= 2:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    start1, end1 = positions[i], positions[i] + len(word) - 1
                    start2, end2 = positions[j], positions[j] + len(word) - 1
                    if start2 > end1:
                        abbreviations = [(start1, end1), (start2, end2)]
                        min_length = min(min_length, calculate_length(abbreviations))
    
    # If no abbreviation was found, return the original length
    if min_length == float('inf'):
        min_length = sum(len(word) for word in words)
    
    return min_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
words = data[1:]

# Calculate and print the result
result = min_length_after_abbreviation(n, words)
print(result)