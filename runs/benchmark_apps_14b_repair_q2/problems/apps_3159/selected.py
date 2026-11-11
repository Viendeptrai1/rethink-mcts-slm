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
                image = []
                stack = [(i, j)]
                visited[i][j] = True
                
                while stack:
                    x, y = stack.pop()
                    image.append((x, y))
                    
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and page[nx][ny] == '+' and not visited[nx][ny]:
                            stack.append((nx, ny))
                            visited[nx][ny] = True
                
                images.append(image)
    
    return images

def get_image_boundaries(image):
    min_x = min(p[0] for p in image)
    max_x = max(p[0] for p in image)
    min_y = min(p[1] for p in image)
    max_y = max(p[1] for p in image)
    return min_x, max_x, min_y, max_y

def contains_banned_char(page, image):
    for x, y in image:
        if not is_valid_char(page[x][y]):
            return True
    return False

def remove_ad(page, image):
    min_x, max_x, min_y, max_y = get_image_boundaries(image)
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            page[x][y] = ' '

def process_page(page, H, W):
    images = find_images(page, H, W)
    ads = []
    
    for image in images:
        if contains_banned_char(page, image):
            ads.append((image, len(image)))
    
    ads.sort(key=lambda x: x[1])
    
    for image, _ in ads:
        remove_ad(page, image)
    
    return page

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    H, W = map(int, data[0].split())
    page = [list(line) for line in data[1:]]
    
    processed_page = process_page(page, H, W)
    
    for row in processed_page:
        print(''.join(row))

if __name__ == "__main__":
    main()