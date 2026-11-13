def find_lexicographically_smallest_word():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    R, C = map(int, data[0].split())
    crossword = [list(data[i+1]) for i in range(R)]

    def extract_words():
        words = []
        
        # Extract horizontal words
        for row in crossword:
            word = ''
            for char in row:
                if char != '#':
                    word += char
                else:
                    if len(word) >= 2:
                        words.append(word)
                    word = ''
            if len(word) >= 2:
                words.append(word)
        
        # Extract vertical words
        for col in range(C):
            word = ''
            for row in range(R):
                char = crossword[row][col]
                if char != '#':
                    word += char
                else:
                    if len(word) >= 2:
                        words.append(word)
                    word = ''
            if len(word) >= 2:
                words.append(word)
        
        return words

    words = extract_words()
    smallest_word = min(words)
    print(smallest_word)

# The function assumes it will be called with input from stdin
find_lexicographically_smallest_word()