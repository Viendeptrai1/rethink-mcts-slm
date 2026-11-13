def count_grey_cells(R, C, K):
    def is_white_cell(r, c):
        return bin(r).count('1') > 0 or bin(c).count('1') > 0

    grey_cells_count = 0
    steps = 0
    r, c = 0, 0
    direction = 'down'

    while steps < K:
        if is_white_cell(r, c):
            grey_cells_count += 1
        
        if direction == 'down':
            if r == R - 1 or (r < R - 1 and is_white_cell(r + 1, c)):
                direction = 'up'
            else:
                r += 1
        elif direction == 'up':
            if r == 0 or (r > 0 and is_white_cell(r - 1, c)):
                direction = 'down'
            else:
                r -= 1

        c += 1
        steps += 1

    return grey_cells_count

import sys

def main():
    input_data = sys.stdin.read().strip().split()
    R = int(input_data[0])
    C = int(input_data[1])
    K = int(input_data[2])
    
    result = count_grey_cells(R, C, K)
    print(result)

if __name__ == "__main__":
    main()