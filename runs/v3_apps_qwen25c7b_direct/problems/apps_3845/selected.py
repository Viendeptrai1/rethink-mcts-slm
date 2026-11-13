import sys

def generate_grid(A, B):
    if A == 1 and B == 1:
        return "1 1\n#"
    
    if A == 1:
        return f"{B+1} {B+1}\n{''.join(['#'*(i%2==0) + '.'*(i%2!=0) for i in range(B)])}"
    
    if B == 1:
        return f"{A+1} {A+1}\n{''.join(['.'*(i%2==0) + '#'*(i%2!=0) for i in range(A)])}"
    
    h = A + B - 1
    w = max(A, B)
    grid = [['.' for _ in range(w)] for _ in range(h)]
    
    def paint_white(x, y):
        if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] != '.':
            return
        grid[x][y] = '#'
        paint_black(x-1, y)
        paint_black(x+1, y)
        paint_black(x, y-1)
        paint_black(x, y+1)
    
    def paint_black(x, y):
        if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] != '#':
            return
        grid[x][y] = '.'
        paint_white(x-1, y)
        paint_white(x+1, y)
        paint_white(x, y-1)
        paint_white(x, y+1)
    
    for i in range(A):
        paint_white(i, i)
    
    for i in range(B):
        paint_black(i, A+i)
    
    return f"{h} {w}\n" + '\n'.join(''.join(row) for row in grid)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    result = generate_grid(A, B)
    print(result)