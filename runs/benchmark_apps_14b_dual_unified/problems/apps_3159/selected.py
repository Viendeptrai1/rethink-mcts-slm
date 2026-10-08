import sys

def is_ad(image):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!,.")
    for row in image:
        for char in row:
            if char not in allowed_chars:
                return True
    return False

def remove_ads(H, W, webpage):
    result = [[' ' for _ in range(W)] for _ in range(H)]
    visited = [[False for _ in range(W)] for _ in range(H)]
    
    def get_image(x, y):
        image = []
        stack = [(x, y)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while stack:
            cx, cy = stack.pop()
            if visited[cx][cy]:
                continue
            visited[cx][cy] = True
            image.append((cx, cy))
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < H and 0 <= ny < W and webpage[nx][ny] == '+':
                    stack.append((nx, ny))
        
        return image
    
    for i in range(H):
        for j in range(W):
            if webpage[i][j] == '+' and not visited[i][j]:
                image = get_image(i, j)
                image_content = []
                for x, y in image:
                    image_content.append(webpage[x][y])
                
                if is_ad(image_content):
                    for x, y in image:
                        result[x][y] = ' '
    
    return [''.join(row) for row in result]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    webpage = data[2:]
    
    result = remove_ads(H, W, webpage)
    for line in result:
        print(line)

if __name__ == "__main__":
    main()