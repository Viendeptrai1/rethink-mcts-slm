import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        H, W = map(int, input_data[0].split())
    except ValueError:
        return

    grid = [list(line) for line in input_data[1:H+1]]

    # Find all images
    # An image is a rectangle of '+' on the border, at least 3x3.
    # '+' characters belong to exactly one image border.
    # Borders are not adjacent (not even at corners).
    
    images = []
    
    # We need to identify the bounding box of each image.
    # Since borders don't touch (even corners), we can scan for '+' and try to expand.
    # However, a simpler approach for "no touching borders" is:
    # Find the top-left most '+' that is part of an image. Expand right/down to find the full box.
    # But we need to be careful not to include '+' from other images if they were touching (which is forbidden).
    # Since they don't touch, finding a '+' and expanding to the extent of that specific image is safe.
    
    visited_plus = set()
    
    for r in range(H):
        for c in range(W):
            if grid[r][c] == '+' and (r, c) not in visited_plus:
                # This '+' must be part of an image.
                # Find the extent of this image.
                # Since borders don't touch, we can just expand until we hit a non-border '+' or edge.
                # But we know the shape is a rectangle.
                # We need to find min_r, max_r, min_c, max_c for this specific image.
                
                # Start from this point, assume it's top-left or somewhere on the border.
                # Actually, since it's a rectangle, we can scan right to find the right edge of this component.
                # But a '+' might be on the top, bottom, left, or right edge.
                
                # Strategy: 
                # 1. Scan right from (r,c) to find the rightmost column index where this specific '+' chain exists?
                # No, simpler: The problem states borders don't touch. So the '+' we found is isolated from other image borders.
                # We can treat this as a connected component of '+'? 
                # Wait, borders are connected internally. Yes, the border of one image is a connected cycle of '+'.
                # And since borders don't touch, the '+' of image A are never adjacent (8-way) to '+' of image B.
                # So we can do a BFS/DFS to find all '+' belonging to this image.
                
                component = []
                queue = [(r, c)]
                visited_plus.add((r, c))
                component.append((r, c))
                
                while queue:
                    cr, cc = queue.pop(0)
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < H and 0 <= nc < W:
                            if grid[nr][nc] == '+' and (nr, nc) not in visited_plus:
                                visited_plus.add((nr, nc))
                                component.append((nr, nc))
                                queue.append((nr, nc))
                
                # Now we have all '+' for this image. Determine the bounding box.
                min_r = min(x[0] for x in component)
                max_r = max(x[0] for x in component)
                min_c = min(x[1] for x in component)
                max_c = max(x[1] for x in component)
                
                # Validate: It must be at least 3x3.
                if (max_r - min_r + 1) < 3 or (max_c - min_c + 1) < 3:
                    # This shouldn't happen if it's a valid image, but just in case skip.
                    continue
                
                # Check if it's actually a rectangle border.
                # The problem says "All images will follow these rules", so we can assume validity.
                # But we must ensure that the interior doesn't contain '+' that belong to THIS image (impossible by geometry)
                # or that the border is consistent.
                # Given the problem constraints, we can trust the component extraction.
                
                images.append({'r': min_r, 'c': min_c, 'h': max_r - min_r + 1, 'w': max_c - min_c + 1})

    # Now we have a list of images. Some might contain other images.
    # We need to find banned characters inside images.
    # A character is banned if it is NOT in the allowed set: alphanumeric, '?', '!', ',', '.', ' '.
    # For every banned character found inside at least one image, the SMALLEST image (by pixel count = h*w) 
    # that contains that character is flagged for removal.
    
    # Allowed characters set
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!., ")
    
    # Map from banned_char -> list of image_indices that contain it
    banned_containers = {}
    
    # We need to process images. Note: "They can contain other images".
    # The content of an image includes whatever is inside its border.
    # If an inner image is present, its content is also part of the outer image's content?
    # The rule says: "For every banned character that is found inside at least one image..."
    # If a banned char is inside an inner image, it is inside the outer image too.
    # So we need to scan the grid within the bounds of each image.
    
    # First, let's identify which images contain banned characters.
    # We iterate through each image, scan its interior (excluding its own border? or including?)
    # "inside at least one image". Usually, "inside" means within the bounding box.
    # The border itself is '+', which is allowed.
    # So we scan from min_r+1 to max_r-1 and min_c+1 to max_c-1.
    
    # However, if there are nested images, the inner image's border is also '+'.
    # The banned char could be inside the inner image.
    # We just need to check every cell (r, c) where min_r < r < max_r and min_c < c < max_c.
    
    image_pixels = []
    for i, img in enumerate(images):
        h, w = img['h'], img['w']
        pixels = h * w
        image_pixels.append((pixels, i))
    
    # Sort images by pixel count to help with "smallest image" logic later?
    # Or we can just store the mapping and resolve.
    
    # Let's create a map: banned_char -> set of image_indices
    char_to_images = {}
    
    # Sort images by size? No, we need to find the smallest containing the char.
    # Let's just collect all (image_index, char) pairs for banned chars.
    
    # Pre-calculate image sizes for quick lookup
    img_sizes = {i: img['h'] * img['w'] for i, img in enumerate(images)}
    
    # Scan each image
    for idx, img in enumerate(images):
        r_start, c_start = img['r'], img['c']
        h, w = img['h'], img['w']
        
        # Scan interior
        for r in range(r_start + 1, r_start + h - 1):
            for c in range(c_start + 1, c_start + w - 1):
                char = grid[r][c]
                if char not in allowed:
                    # This is a banned character
                    if char not in char_to_images:
                        char_to_images[char] = set()
                    char_to_images[char].add(idx)

    # Now, for each banned character, find the image with the minimum pixel count that contains it.
    images_to_remove = set()
    
    for char, img_set in char_to_images.items():
        # Find image with min pixels
        min_pixels = float('inf')
        best_idx = -1
        for idx in img_set:
            size = img_sizes[idx]
            if size < min_pixels:
                min_pixels = size
                best_idx = idx
        if best_idx != -1:
            images_to_remove.add(best_idx)

    # Remove the images
    # "When an ad is removed, every character inside the ad and the border is replaced with a whitespace."
    for idx in images_to_remove:
        img = images[idx]
        r_start, c_start = img['r'], img['c']
        h, w = img['h'], img['w']
        
        for r in range(r_start, r_start + h):
            for c in range(c_start, c_start + w):
                grid[r][c] = ' '

    # Output the result
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    solve()