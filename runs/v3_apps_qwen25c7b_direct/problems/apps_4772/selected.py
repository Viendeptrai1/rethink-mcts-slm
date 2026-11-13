import sys

def find_smallest_word(R, C, grid):
    smallest_word = "z" * 21
    
    # Check horizontal words
    for row in range(R):
        current_word = ""
        for col in range(C):
            if grid[row][col] != '#':
                current_word += grid[row][col]
            else:
                if len(current_word) >= 2 and current_word < smallest_word:
                    smallest_word = current_word
                current_word = ""
        if len(current_word) >= 2 and current_word < smallest_word:
            smallest_word = current_word
    
    # Check vertical words
    for col in range(C):
        current_word = ""
        for row in range(R):
            if grid[row][col] != '#':
                current_word += grid[row][col]
            else:
                if len(current_word) >= 2 and current_word < smallest_word:
                    smallest_word = current_word
                current_word = ""
        if len(current_word) >= 2 and current_word < smallest_word:
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