import sys

def count_grey_cells(R, C, K):
    def is_grey(row, col):
        return (row & col) == 0

    grey_count = 0
    row, col = 0, 0
    direction = 1  # 1 for right, -1 for left

    for _ in range(K):
        if is_grey(row, col):
            grey_count += 1
        
        if direction == 1:
            col += 1
            if col == C:
                row += 1
                direction = -1
        else:
            col -= 1
            if col == -1:
                row += 1
                direction = 1

    return grey_count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    K = int(data[2])
    
    result = count_grey_cells(R, C, K)
    print(result)

if __name__ == "__main__":
    main()