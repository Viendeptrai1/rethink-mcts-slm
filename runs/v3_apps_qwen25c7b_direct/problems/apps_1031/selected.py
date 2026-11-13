import sys

def draw_cardiogram(a):
    total_sum = sum(a)
    max_height = max(abs(sum(a[:i+1])) for i in range(len(a)))
    height = max_height * 2 + 1
    width = total_sum * 2 + 1
    
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    x, y = width // 2, height // 2
    for i in range(len(a)):
        if i % 2 == 0:
            dx, dy = 1, -1
        else:
            dx, dy = 1, 1
        
        for j in range(1, a[i] + 1):
            nx, ny = x + dx * j, y + dy * j
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                break
            grid[ny][nx] = '/' if dx > 0 else '\\'
        
        x += a[i]
    
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    draw_cardiogram(a)