def remove_ads(H, W, web_page):
    def is_valid_char(c):
        return c.isalnum() or c in "?!,." or c == " "

    def is_border(x, y):
        return web_page[x][y] == "+"

    def is_image(x, y):
        if not is_border(x, y):
            return False
        queue = [(x, y)]
        visited = set()
        while queue:
            px, py = queue.pop(0)
            if (px, py) in visited:
                continue
            visited.add((px, py))
            if not is_valid_char(web_page[px][py]):
                return True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = px + dx, py + dy
                if 0 <= nx < H and 0 <= ny < W and is_border(nx, ny) and (nx, ny) not in visited:
                    queue.append((nx, ny))
        return False

    def clear_image(x, y):
        queue = [(x, y)]
        visited = set()
        while queue:
            px, py = queue.pop(0)
            if (px, py) in visited:
                continue
            visited.add((px, py))
            web_page[px] = web_page[px][:py] + " " * len(web_page[px][py]) + web_page[px][py + 1:]
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = px + dx, py + dy
                if 0 <= nx < H and 0 <= ny < W and is_border(nx, ny) and (nx, ny) not in visited:
                    queue.append((nx, ny))

    for i in range(1, H-1):
        for j in range(1, W-1):
            if is_image(i, j):
                clear_image(i, j)

    return "\n".join("".join(row) for row in web_page)

# Example usage:
import sys
input = sys.stdin.read
data = input().splitlines()
H = int(data[0].split()[0])
W = int(data[0].split()[1])
web_page = data[1:]
result = remove_ads(H, W, web_page)
print(result)