def remove_ads(H, W, webpage):
    def is_valid_char(c):
        return c.isalnum() or c in "?!., "

    def find_images():
        images = []
        visited = set()
        for i in range(H):
            for j in range(W):
                if (i, j) not in visited and webpage[i][j] == '+':
                    image = []
                    queue = [(i, j)]
                    while queue:
                        x, y = queue.pop()
                        if (x, y) in visited:
                            continue
                        visited.add((x, y))
                        image.append((x, y))
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < H and 0 <= ny < W and webpage[nx][ny] == '+':
                                queue.append((nx, ny))
                    images.append(image)
        return images

    def get_image_boundaries(image):
        min_x = min(p[0] for p in image)
        max_x = max(p[0] for p in image)
        min_y = min(p[1] for p in image)
        max_y = max(p[1] for p in image)
        return min_x, max_x, min_y, max_y

    def is_ad(image):
        for x, y in image:
            if not is_valid_char(webpage[x][y]):
                return True
        return False

    def remove_image(image):
        min_x, max_x, min_y, max_y = get_image_boundaries(image)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                webpage[x] = webpage[x][:y] + ' ' + webpage[x][y+1:]

    images = find_images()
    ads = []
    for image in images:
        if is_ad(image):
            ads.append((image, len(image)))

    ads.sort(key=lambda x: x[1])
    for image, _ in ads:
        remove_image(image)

    return '\n'.join(webpage)

# Read input
import sys
input = sys.stdin.read
data = input().splitlines()
H, W = map(int, data[0].split())
webpage = data[1:]

# Process and print result
result = remove_ads(H, W, webpage)
print(result)