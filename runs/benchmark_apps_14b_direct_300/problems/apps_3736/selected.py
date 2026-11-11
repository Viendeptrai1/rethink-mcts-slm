def is_mirror_word(word):
    # Define the mirror mapping for each letter
    mirror_mapping = {
        'A': 'A', 'E': '3', 'H': 'H', 'I': 'I', 'J': 'L',
        'L': 'J', 'M': 'M', 'O': 'O', 'S': '2', 'T': 'T',
        'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
        'Z': '5', '1': '1', '2': 'S', '3': 'E', '5': 'Z',
        '8': '8'
    }
    
    # Check if the word is a mirror word
    n = len(word)
    for i in range(n // 2 + 1):
        if word[i] not in mirror_mapping or word[n - i - 1] != mirror_mapping[word[i]]:
            return "NO"
    return "YES"

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Print the result
print(is_mirror_word(input))