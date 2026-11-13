import sys

def find_smallest_word(R, C, grid):
    smallest_word = None
    
    # Check rows
    for i in range(R):
        current_word = ""
        for j in range(C):
            if grid[i][j] != '#':
                current_word += grid[i][j]
            else:
                if len(current_word) >= 2:
                    if smallest_word is None or current_word < smallest_word:
                        smallest_word = current_word
                current_word = ""
        if len(current_word) >= 2:
            if smallest_word is None or current_word < smallest_word:
                smallest_word = current_word
    
    # Check columns
    for j in range(C):
        current_word = ""
        for i in range(R):
            if grid[i][j] != '#':
                current_word += grid[i][j]
            else:
                if len(current_word) >= 2:
                    if smallest_word is None or current_word < smallest_word:
                        smallest_word = current_word
                current_word = ""
        if len(current_word) >= 2:
            if smallest_word is None or current_word < smallest_word:
                smallest_word = current_word
    
    return smallest_word

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    grid = [data[i + 2] for i in range(R)]
    
    result = find_smallest_word(R, C, grid)
    print(result)