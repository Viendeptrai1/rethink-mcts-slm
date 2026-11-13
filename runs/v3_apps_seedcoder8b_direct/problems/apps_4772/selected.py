def find_lexicographically_smallest_word():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    R, C = map(int, data[0].split())
    crossword = [list(data[i + 1]) for i in range(R)]
    
    def extract_words():
        words = []
        
        # Extract horizontal words
        for row in crossword:
            word = []
            for char in row:
                if char == '#':
                    if len(word) >= 2:
                        words.append(''.join(word))
                    word = []
                else:
                    word.append(char)
            if len(word) >= 2:
                words.append(''.join(word))
        
        # Extract vertical words
        for col in range(C):
            word = []
            for row in range(R):
                char = crossword[row][col]
                if char == '#':
                    if len(word) >= 2:
                        words.append(''.join(word))
                    word = []
                else:
                    word.append(char)
            if len(word) >= 2:
                words.append(''.join(word))
        
        return words
    
    words = extract_words()
    smallest_word = min(words)
    print(smallest_word)