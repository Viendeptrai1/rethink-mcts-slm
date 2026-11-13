def remove_ads(H, W, grid):
    def is_valid_image(x, y, w, h):
        if x < 0 or y < 0 or x + w > W or y + h > H:
            return False
        for i in range(w):
            if grid[y][x+i] != '+' or grid[y+h-1][x+i] != '+':
                return False
        for j in range(h):
            if grid[y+j][x] != '+' or grid[y+j][x+w-1] != '+':
                return False
        return True

    def find_images():
        images = []
        visited = [[False] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                if grid[y][x] == '+' and not visited[y][x]:
                    w, h = 1, 1
                    while x + w < W and grid[y][x+w] == '+':
                        w += 1
                    while y + h < H and grid[y+h][x] == '+':
                        h += 1
                    if is_valid_image(x, y, w, h):
                        images.append((x, y, w, h))
                        for i in range(y, y+h):
                            for j in range(x, x+w):
                                visited[i][j] = True
        return images

    def remove_image(x, y, w, h):
        for i in range(y, y+h):
            for j in range(x, x+w):
                grid[i][j] = ' '

    images = find_images()
    for x, y, w, h in images:
        remove_image(x, y, w, h)

    return ''.join(''.join(row) for row in grid)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
H = int(data[0])
W = int(data[1])
grid = [list(data[i+2]) for i in range(H)]
result = remove_ads(H, W, grid)
print(result)