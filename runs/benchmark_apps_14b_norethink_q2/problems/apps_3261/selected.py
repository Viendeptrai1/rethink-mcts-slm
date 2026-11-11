import sys

def count_grey_cells(R, C, K):
    def is_grey(row, col):
        return any((row & (1 << i)) == (col & (1 << i)) == 0 for i in range(32))

    grey_count = 0
    current_row = 0
    direction = 1  # 1 for right, -1 for left

    for step in range(K):
        if is_grey(current_row, step % C):
            grey_count += 1
        
        if (step % C == C - 1 and direction == 1) or (step % C == 0 and direction == -1):
            current_row += 1
            direction *= -1

    return grey_count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    K = int(data[2])
    
    result = count_grey_cells(R, C, K)
    print(result)