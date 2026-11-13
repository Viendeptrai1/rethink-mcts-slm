def remove_ads(H, W, web_page):
    from collections import defaultdict

    def is_border(r, c):
        return (r == 0 or r == H - 1 or c == 0 or c == W - 1 or
                web_page[r][c] == '+')

    def find_image_borders():
        borders = []
        visited = [[False] * W for _ in range(H)]
        for r in range(H):
            for c in range(W):
                if web_page[r][c] == '+' and not visited[r][c]:
                    # Start of a new image
                    br, bc = r, c
                    while br < H and web_page[br][c] == '+':
                        br += 1
                    while bc < W and web_page[r][bc] == '+':
                        bc += 1
                    br -= 1
                    bc -= 1
                    if br - r >= 2 and bc - c >= 2:
                        borders.append((r, c, br, bc))
                    for vr in range(r, br + 1):
                        for vc in range(c, bc + 1):
                            visited[vr][vc] = True
        return borders

    def is_valid_image(r1, c1, r2, c2):
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if is_border(r, c):
                    continue
                if not (web_page[r][c].isalnum() or web_page[r][c] in '?!,. '):
                    return False
        return True

    def remove_image(r1, c1, r2, c2):
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                web_page[r][c] = ' '

    def find_smallest_image_with_char(char):
        min_area = float('inf')
        smallest_image = None
        for r1, c1, r2, c2 in image_borders:
            if is_valid_image(r1, c1, r2, c2):
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        if web_page[r][c] == char:
                            area = (r2 - r1 + 1) * (c2 - c1 + 1)
                            if area < min_area:
                                min_area = area
                                smallest_image = (r1, c1, r2, c2)
        return smallest_image

    image_borders = find_image_borders()
    banned_chars = set()

    for r in range(H):
        for c in range(W):
            if web_page[r][c] not in ' +' and not web_page[r][c].isalnum() and web_page[r][c] not in '?!,. ':
                banned_chars.add(web_page[r][c])

    for char in banned_chars:
        image_to_remove = find_smallest_image_with_char(char)
        if image_to_remove:
            remove_image(*image_to_remove)

    return ''.join(''.join(row) for row in web_page)

import sys
input = sys.stdin.read
data = input().splitlines()
H, W = map(int, data[0].split())
web_page = [list(line) for line in data[1:]]
result = remove_ads(H, W, web_page)
print(result)