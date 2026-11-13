def count_grey_cells(R, C, K):
    def is_white_cell(r, c):
        return bin(r).count('1') > 0 or bin(c).count('1') > 0

    grey_count = 0
    x, y = 0, 0
    dx, dy = 1, 1

    for _ in range(K):
        if is_white_cell(x, y):
            grey_count += 1

        if x + dx < 0 or x + dx >= R:
            dx = -dx
        if y + dy < 0 or y + dy >= C:
            dy = -dy

        x += dx
        y += dy

    return grey_count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    R = int(data[0])
    C = int(data[1])
    K = int(data[2])
    print(count_grey_cells(R, C, K))