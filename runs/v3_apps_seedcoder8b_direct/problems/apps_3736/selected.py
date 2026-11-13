def is_mirror_word(word):
    # Define the mirror reflection of each letter
    mirror_map = {
        'A': 'A', 'H': 'H', 'I': 'I', 'M': 'M', 'O': 'O', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
        'E': '3', '3': 'E',
        'B': '8', '8': 'B',
        'P': 'D', 'D': 'P'
    }
    
    # Check if the word is a mirror word
    n = len(word)
    for i in range(n):
        if word[i] not in mirror_map or mirror_map[word[i]] != word[n - 1 - i]:
            return 'NO'
    return 'YES'

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(is_mirror_word(input))