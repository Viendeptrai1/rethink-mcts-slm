import sys

def is_banned_char(c):
    return not (c.isalnum() or c in "?!., ")

def find_images(page, H, W):
    images = []
    visited = set()
    
    for i in range(H):
        for j in range(W):
            if page[i][j] == '+' and (i, j) not in visited:
                # Start of a new image
                image = []
                stack = [(i, j)]
                visited.add((i, j))
                
                while stack:
                    x, y = stack.pop()
                    image.append((x, y))
                    
                    # Explore neighbors
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and page[nx][ny] == '+' and (nx, ny) not in visited:
                            stack.append((nx, ny))
                            visited.add((nx, ny))
                
                images.append(image)
    
    return images

def get_image_content(page, image):
    min_x = min(x for x, y in image)
    max_x = max(x for x, y in image)
    min_y = min(y for x, y in image)
    max_y = max(y for x, y in image)
    
    content = []
    for i in range(min_x, max_x + 1):
        row = []
        for j in range(min_y, max_y + 1):
            row.append(page[i][j])
        content.append(row)
    
    return content

def has_banned_char(content):
    for row in content:
        for char in row:
            if is_banned_char(char):
                return True
    return False

def remove_ads(page, H, W):
    images = find_images(page, H, W)
    ads_to_remove = []
    
    for image in images:
        content = get_image_content(page, image)
        if has_banned_char(content):
            ads_to_remove.append(image)
    
    # Remove the smallest ad first
    ads_to_remove.sort(key=lambda img: len(img))
    
    for image in ads_to_remove:
        min_x = min(x for x, y in image)
        max_x = max(x for x, y in image)
        min_y = min(y for x, y in image)
        max_y = max(y for x, y in image)
        
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                page[i][j] = ' '
    
    return page

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    H, W = map(int, data[0].split())
    page = [list(line) for line in data[1:]]
    
    result = remove_ads(page, H, W)
    
    for row in result:
        print(''.join(row))

if __name__ == "__main__":
    main()