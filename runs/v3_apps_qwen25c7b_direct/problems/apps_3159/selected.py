def remove_ads(H, W, web_page):
    import sys
    input = sys.stdin.read
    data = input().split()
    
    def is_valid_char(c):
        return c.isalnum() or c in '?!,.'
    
    def is_border_char(c):
        return c == '+'
    
    def is_banned_char(c):
        return not is_valid_char(c)
    
    def get_image_size(x, y):
        if not (is_border_char(web_page[x][y]) and is_border_char(web_page[x-1][y]) and 
                is_border_char(web_page[x][y-1]) and is_border_char(web_page[x-1][y-1])):
            return float('inf')
        
        size = 0
        queue = [(x, y)]
        visited = set()
        visited.add((x, y))
        
        while queue:
            cx, cy = queue.pop(0)
            size += 1
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < H and 0 <= ny < W and (nx, ny) not in visited and is_border_char(web_page[nx][ny]):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        
        return size
    
    def remove_ad(x, y):
        queue = [(x, y)]
        visited = set()
        visited.add((x, y))
        
        while queue:
            cx, cy = queue.pop(0)
            web_page[cx] = web_page[cx][:cy] + ' ' * len(web_page[cx][cy:]) + web_page[cx][cy:]
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < H and 0 <= ny < W and (nx, ny) not in visited and is_border_char(web_page[nx][ny]):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
    
    min_size = float('inf')
    ad_positions = []
    
    for i in range(1, H-1):
        for j in range(1, W-1):
            if is_border_char(web_page[i][j]) and is_border_char(web_page[i-1][j]) and \
               is_border_char(web_page[i][j-1]) and is_border_char(web_page[i-1][j-1]):
                size = get_image_size(i, j)
                if size < min_size:
                    min_size = size
                    ad_positions = [(i, j)]
                elif size == min_size:
                    ad_positions.append((i, j))
    
    for x, y in ad_positions:
        remove_ad(x, y)
    
    result = '\n'.join(web_page)
    print(result)

# Example usage:
# H, W = map(int, input().split())
# web_page = [input().strip() for _ in range(H)]
# remove_ads(H, W, web_page)