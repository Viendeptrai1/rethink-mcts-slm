def is_mirror_word(word):
    # Dictionary mapping each letter to its mirror image counterpart
    mirror_map = {
        'A': 'A', 'E': '3', 'H': 'H', 'I': 'I', 'J': 'L',
        'L': 'J', 'M': 'M', 'O': 'O', 'S': '2', 'T': 'T',
        'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
        'Z': '5', '1': '1', '2': 'S', '3': 'E', '5': 'Z',
        '8': '8'
    }
    
    # Check if all characters in the word have a mirror image counterpart
    mirrored_word = ''.join(mirror_map.get(char, '') for char in word)
    
    # If the length of the mirrored word is not the same as the original, it's not a mirror word
    if len(mirrored_word) != len(word):
        return 'NO'
    
    # Check if the mirrored word is the reverse of the original word
    if mirrored_word == word[::-1]:
        return 'YES'
    else:
        return 'NO'

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Print the result
print(is_mirror_word(input))