import sys

def generate_grid(A, B):
    if A == 1 and B == 1:
        return "1 1\n."
    
    h = A + B
    w = max(2 * min(A, B), 3)
    
    grid = [['.' for _ in range(w)] for _ in range(h)]
    
    def paint_row(row, color):
        for i in range(w):
            if (i // 2) % 2 == row % 2:
                grid[row][i] = color
    
    for i in range(A):
        paint_row(i, '#')
    
    for i in range(B):
        paint_row(i + A, '.')
    
    return f"{h} {w}\n" + '\n'.join(''.join(row) for row in grid)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    result = generate_grid(A, B)
    print(result)