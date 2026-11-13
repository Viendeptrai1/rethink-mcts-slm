def remove_ads(H, W, web_page):
    from collections import deque

    # Helper function to check if a character is allowed
    def is_allowed_char(c):
        return c.isalnum() or c in {'?', '!', ',', '.', ' '}

    # Helper function to find all images
    def find_images():
        images = []
        visited = [[False] * W for _ in range(H)]

        for i in range(H):
            for j in range(W):
                if web_page[i][j] == '+' and not visited[i][j]:
                    # BFS to find the full image
                    queue = deque([(i, j)])
                    visited[i][j] = True
                    min_i, max_i, min_j, max_j = i, i, j, j

                    while queue:
                        x, y = queue.popleft()
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny] and web_page[nx][ny] == '+':
                                visited[nx][ny] = True
                                queue.append((nx, ny))
                                min_i, max_i = min(min_i, nx), max(max_i, nx)
                                min_j, max_j = min(min_j, ny), max(max_j, ny)

                    images.append((min_i, max_i, min_j, max_j))

        return images

    # Find all images
    images = find_images()

    # Check each image for banned characters
    for min_i, max_i, min_j, max_j in images:
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                if not is_allowed_char(web_page[i][j]):
                    # Found a banned character, mark this image for removal
                    for x in range(min_i, max_i + 1):
                        for y in range(min_j, max_j + 1):
                            web_page[x] = web_page[x][:y] + ' ' + web_page[x][y+1:]
                    break
            else:
                continue
            break

    # Print the modified web page
    for line in web_page:
        print(line)

# Read input
import sys
input = sys.stdin.read
data = input().splitlines()
H, W = map(int, data[0].split())
web_page = data[1:]

# Call the function
remove_ads(H, W, web_page)