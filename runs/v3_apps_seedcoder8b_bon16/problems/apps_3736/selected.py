def is_mirror_word(name):
    # Define the mirror map for uppercase English letters
    mirror_map = {
        'A': 'A', 'H': 'H', 'I': 'I', 'M': 'M', 'O': 'O', 'T': 'T', 'U': 'U', 'V': 'V', 
        'W': 'W', 'X': 'X', 'Y': 'Y',
        'E': '3', '3': 'E',
        'B': '8', '8': 'B',
        'P': 'D', 'D': 'P'
    }
    
    # Initialize an empty list to store mirrored characters
    mirrored_chars = []
    
    # Iterate over each character in the name
    for char in reversed(name):
        if char in mirror_map:
            mirrored_chars.append(mirror_map[char])
        else:
            return 'NO'
    
    # Compare the mirrored string with the original string
    return 'YES' if ''.join(mirrored_chars) == name else 'NO'

# Read input from standard input
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(is_mirror_word(input))