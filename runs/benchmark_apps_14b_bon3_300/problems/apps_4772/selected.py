import sys

def find_lexicographically_smallest_word(R, C, grid):
    def get_words():
        words = []
        # Check horizontal words
        for r in range(R):
            current_word = ""
            for c in range(C):
                if grid[r][c] != '#':
                    current_word += grid[r][c]
                else:
                    if len(current_word) >= 2:
                        words.append(current_word)
                    current_word = ""
            if len(current_word) >= 2:
                words.append(current_word)
        
        # Check vertical words
        for c in range(C):
            current_word = ""
            for r in range(R):
                if grid[r][c] != '#':
                    current_word += grid[r][c]
                else:
                    if len(current_word) >= 2:
                        words.append(current_word)
                    current_word = ""
            if len(current_word) >= 2:
                words.append(current_word)
        
        return words

    words = get_words()
    words.sort()
    return words[0]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    grid = data[2:]
    
    result = find_lexicographically_smallest_word(R, C, grid)
    print(result)

if __name__ == "__main__":
    main()