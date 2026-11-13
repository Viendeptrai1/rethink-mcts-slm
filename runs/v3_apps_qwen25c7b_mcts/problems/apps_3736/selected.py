def is_mirror_word(word):
    mirror_map = {
        'A': 'A', 'B': '', 'C': '', 'D': '', 'E': '3', 'F': '',
        'G': '', 'H': 'H', 'I': 'I', 'J': '', 'K': '', 'L': '',
        'M': 'M', 'N': '', 'O': 'O', 'P': '', 'Q': '', 'R': '',
        'S': '2', 'T': 'T', 'U': 'U', 'V': 'V', 'W': '', 'X': 'X',
        'Y': 'Y', 'Z': '5'
    }
    
    mirrored_word = ''.join(mirror_map[char] for char in reversed(word))
    return word == mirrored_word

# Example usage:
if __name__ == "__main__":
    import sys
    word = sys.stdin.read().strip()
    result = "YES" if is_mirror_word(word) else "NO"
    print(result)