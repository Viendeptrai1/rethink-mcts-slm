def find_smallest_word(R, C, crossword):
    min_word = 'z' * 20
    
    # Check horizontal words
    for row in range(R):
        word = ''
        for col in range(C):
            if crossword[row][col] != '#':
                word += crossword[row][col]
            else:
                if len(word) >= 2 and word < min_word:
                    min_word = word
                word = ''
        if len(word) >= 2 and word < min_word:
            min_word = word
    
    # Check vertical words
    for col in range(C):
        word = ''
        for row in range(R):
            if crossword[row][col] != '#':
                word += crossword[row][col]
            else:
                if len(word) >= 2 and word < min_word:
                    min_word = word
                word = ''
        if len(word) >= 2 and word < min_word:
            min_word = word
    
    return min_word

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    crossword = data[2:]
    
    result = find_smallest_word(R, C, crossword)
    print(result)