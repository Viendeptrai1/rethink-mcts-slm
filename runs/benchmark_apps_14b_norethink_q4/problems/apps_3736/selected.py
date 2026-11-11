def is_mirror_word(name):
    # Dictionary mapping each letter to its mirror image counterpart
    mirror_map = {
        'A': 'A', 'E': '3', 'H': 'H', 'I': 'I', 'J': 'L',
        'L': 'J', 'M': 'M', 'O': 'O', 'S': '2', 'T': 'T',
        'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
        'Z': '5', '1': '1', '2': 'S', '3': 'E', '5': 'Z',
        '8': '8'
    }
    
    # Check if all characters in the name have a mirror counterpart
    for char in name:
        if char not in mirror_map:
            return "NO"
    
    # Create the mirrored version of the name
    mirrored_name = ''.join(mirror_map[char] for char in reversed(name))
    
    # Check if the mirrored name is the same as the original name
    if mirrored_name == name:
        return "YES"
    else:
        return "NO"

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Print the result
print(is_mirror_word(input))