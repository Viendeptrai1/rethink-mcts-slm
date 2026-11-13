def is_mirror_word(word):
    # Define the mapping of characters to their mirror reflections
    mirror_map = {
        'A': 'A', 'B': 'N', 'C': 'M', 'D': 'W', 'E': 'M',
        'F': 'X', 'G': 'O', 'H': 'H', 'I': 'I', 'J': 'L',
        'K': 'T', 'L': 'J', 'M': 'C', 'N': 'B', 'O': 'G',
        'P': 'S', 'Q': 'R', 'R': 'Q', 'S': 'P', 'T': 'K',
        'U': 'U', 'V': 'V', 'W': 'D', 'X': 'F', 'Y': 'Y', 'Z': '5'
    }
    
    # Check if the word is a mirror word
    return all(mirror_map[word[i]] == word[-i-1] for i in range(len(word)//2 + 1))

# Read input from stdin
import sys
word = sys.stdin.read().strip()

# Print the result
print('YES' if is_mirror_word(word) else 'NO')