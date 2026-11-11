import sys

def is_valid_char(c):
    return c.isalnum() or c in "?!., "

def find_images(page, H, W):
    images = []
    visited = [[False] * W for _ in range(H)]
    
    for i in range(1, H-1):
        for j in range(1, W-1):
            if page[i][j] == '+' and not visited[i][j]:
                # Start of a new image
                queue = [(i, j)]
                image = []
                visited[i][j] = True
                
                while queue:
                    x, y = queue.pop()
                    image.append((x, y))
                    
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and page[nx][ny] == '+' and not visited[nx][ny]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                
                images.append(image)
    
    return images

def contains_banned_char(image, page):
    for x, y in image:
        if not is_valid_char(page[x][y]):
            return True
    return False

def remove_image(page, image):
    for x, y in image:
        page[x] = page[x][:y] + ' ' + page[x][y+1:]

def process_web_page(H, W, page):
    images = find_images(page, H, W)
    images.sort(key=lambda img: len(img))
    
    for image in images:
        if contains_banned_char(image, page):
            remove_image(page, image)
    
    return '\n'.join(page)

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    H, W = map(int, data[0].split())
    page = data[1:]
    
    result = process_web_page(H, W, page)
    print(result)

if __name__ == "__main__":
    main()