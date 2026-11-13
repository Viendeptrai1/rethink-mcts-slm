def remove_ads():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    H, W = map(int, data[0].split())
    page = data[1:H+1]
    
    # Helper function to find all images
    def find_images():
        images = []
        visited = [[False] * W for _ in range(H)]
        
        def in_bounds(x, y):
            return 0 <= x < H and 0 <= y < W
        
        def is_border(x, y):
            if page[x][y] != '+':
                return False
            # Check if it's a valid border by examining its neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if not in_bounds(nx, ny) or page[nx][ny] != '+':
                    return False
            return True
        
        def find_full_image(x, y):
            # Find the bottom-right corner of the image starting from (x, y)
            # This assumes (x, y) is a valid '+' of an image border
            min_x, max_x = x, x
            min_y, max_y = y, y
            
            # Explore downwards and to the right to find the image boundaries
            for i in range(x, H):
                if page[i][y] == '+':
                    max_x = i
                else:
                    break
            for j in range(y, W):
                if page[x][j] == '+':
                    max_y = j
                else:
                    break
            
            return min_x, min_y, max_x, max_y
        
        for i in range(H):
            for j in range(W):
                if is_border(i, j) and not visited[i][j]:
                    min_x, min_y, max_x, max_y = find_full_image(i, j)
                    images.append((min_x, min_y, max_x, max_y))
                    for x in range(min_x, max_x + 1):
                        for y in range(min_y, max_y + 1):
                            visited[x][y] = True
        
        return images
    
    # Helper function to determine if an image contains any banned character
    def contains_banned_char(image, banned_chars):
        min_x, min_y, max_x, max_y = image
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if page[x][y] in banned_chars:
                    return True
        return False
    
    # Helper function to mark an image as ad by turning it to whitespace
    def mark_as_ad(image):
        min_x, min_y, max_x, max_y = image
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                page[x] = page[x][:y] + ' ' + page[x][y+1:]
    
    # Define the banned characters
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?., ")
    banned_chars = set(chr(i) for i in range(32, 127)) - allowed_chars
    
    # Find and remove ads
    images = find_images()
    for image in images:
        if contains_banned_char(image, banned_chars):
            mark_as_ad(image)
    
    # Print the final web page
    for line in page:
        print(line)