import sys

def find_lexicographically_smallest_word(R, C, grid):
    smallest_word = None
    
    # Check rows for words
    for row in grid:
        current_word = ""
        for char in row:
            if char != '#':
                current_word += char
            else:
                if len(current_word) >= 2:
                    if smallest_word is None or current_word < smallest_word:
                        smallest_word = current_word
                current_word = ""
        if len(current_word) >= 2:
            if smallest_word is None or current_word < smallest_word:
                smallest_word = current_word
    
    # Check columns for words
    for col in range(C):
        current_word = ""
        for row in range(R):
            char = grid[row][col]
            if char != '#':
                current_word += char
            else:
                if len(current_word) >= 2:
                    if smallest_word is None or current_word < smallest_word:
                        smallest_word = current_word
                current_word = ""
        if len(current_word) >= 2:
            if smallest_word is None or current_word < smallest_word:
                smallest_word = current_word
    
    return smallest_word

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