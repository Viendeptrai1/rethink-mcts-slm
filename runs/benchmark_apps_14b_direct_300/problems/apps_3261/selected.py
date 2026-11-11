import sys

def count_grey_cells(R, C, K):
    def is_grey(row, col):
        return any((row & (1 << i)) == (col & (1 << i)) == 0 for i in range(64))

    count = 0
    current_row, current_col = 0, 0
    direction = 1  # 1 for right, -1 for left

    for _ in range(K):
        if is_grey(current_row, current_col):
            count += 1

        if direction == 1:
            if current_col + 1 < C:
                current_col += 1
            else:
                current_row += 1
                direction = -1
        else:
            if current_col - 1 >= 0:
                current_col -= 1
            else:
                current_row += 1
                direction = 1

    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    K = int(data[2])
    
    result = count_grey_cells(R, C, K)
    print(result)