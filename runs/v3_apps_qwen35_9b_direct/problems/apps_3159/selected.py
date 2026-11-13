import sys

def solve():
    input_data = sys.stdin.read().split('\n')
    if not input_data:
        return
    
    first_line = input_data[0].split()
    H, W = int(first_line[0]), int(first_line[1])
    
    grid = []
    for i in range(1, H + 1):
        if i < len(input_data):
            grid.append(input_data[i])
        else:
            grid.append('')
    
    # Ensure all rows are length W
    for i in range(H):
        if len(grid[i]) < W:
            grid[i] += ' ' * (W - len(grid[i]))
        elif len(grid[i]) > W:
            grid[i] = grid[i][:W]
    
    # Allowed characters
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!,. ")
    
    # Find all images
    # An image is a rectangle of '+' on border, size at least 3x3
    # '+' belongs to exactly one image border
    # Borders not adjacent (not even corners)
    
    images = [] # List of (r1, c1, r2, c2)
    visited_plus = set()
    
    # Scan for top-left corners of potential images
    for r in range(H):
        for c in range(W):
            if grid[r][c] == '+':
                # Check if this '+' is already part of an image border
                if (r, c) in visited_plus:
                    continue
                
                # Try to form a rectangle starting at (r, c)
                # The '+' at (r, c) must be the top-left corner of a new image
                # We need to find the bottom-right corner such that:
                # 1. All border cells are '+'
                # 2. Size >= 3x3
                # 3. No other '+' from another image touches this one (including corners)
                
                # First, let's assume this is a top-left corner and try to expand
                # But we need to be careful: the rule says "All '+' characters belong to the border of exactly 1 image"
                # and "Borders of different images will not be adjacent".
                # This implies that if we find a '+' that hasn't been visited, it MUST be the start of a new image.
                # However, a '+' could be top-left, top-right, bottom-left, or bottom-right.
                # But since we scan top-to-bottom, left-to-right, the first time we see a '+' that is part of an image,
                # it must be the top-left corner of that image? Not necessarily.
                # Example:
                # +++++
                # +   +
                # +   +
                # +++++
                # If we scan row 0, col 0, we find '+'. It is top-left.
                # What if we have:
                #   +++++
                #   +   +
                #   +   +
                #   +++++
                # Then at row 0, col 0 we see ' '. At row 0, col 1 we see ' '. At row 0, col 2 we see '+'.
                # This '+' is top-left.
                # So yes, the first '+' we encounter in row-major order that is not visited must be the top-left corner of an image.
                # Why? Because if it were top-right, bottom-left, or bottom-right, there would be a '+' above it or to the left of it
                # that belongs to the same image, which would have been visited already.
                # Exception: What if the image is 3x3 and we are at the top-left? Yes.
                # What if we are at top-right? Then top-left was visited.
                # So the strategy: iterate r, c. If grid[r][c] == '+' and not visited, then this is the top-left of a new image.
                
                # Now, we need to determine the size of this image.
                # We know (r, c) is top-left. We need to find the bottom-right (r2, c2).
                # The border must be all '+'.
                # Also, we must ensure that no other '+' from a different image touches this image.
                # But since we are building images one by one and marking visited, and the problem guarantees valid input structure
                # (borders not adjacent), we can just find the maximal rectangle of '+' that forms a valid image border.
                # However, the problem says "All '+' characters belong to the border of exactly 1 image".
                # This means we cannot have overlapping borders.
                # So, starting from (r, c), we look for the rightmost '+' in row r that is part of the top border.
                # Then from that rightmost point, we look down to find the bottom-right.
                # Then from bottom-right, we look left to find bottom-left.
                # Then from bottom-left, we look up to verify top-left (which we know).
                # And check that all these borders are '+'.
                # Also check that the interior doesn't contain '+' that belong to other images? 
                # Actually, the problem says "They can contain other images". So interior '+' are part of nested images.
                # But the border of the current image must be '+' and not touch any other image's border.
                # Since we process in order and mark visited, and the input is guaranteed to have non-adjacent borders,
                # we can simply find the extent of the current image by scanning.
                
                # Let's find the rightmost '+' in row r starting from c.
                c_right = c
                while c_right + 1 < W and grid[r][c_right + 1] == '+':
                    c_right += 1
                
                # Now we have top edge from c to c_right.
                # Check if this is a valid top edge (length >= 3)
                if c_right - c + 1 < 3:
                    # This shouldn't happen if input is valid and this is a top-left corner
                    # But maybe this '+' is not a top-left corner? 
                    # Wait, if we are at (r, c) and it's '+', and we haven't visited it, it MUST be top-left.
                    # Because if it were not top-left, there would be a '+' to its left or above in the same image.
                    # If above, we would have visited it when scanning that row.
                    # If left, we would have visited it when scanning this row earlier.
                    # So yes, it must be top-left.
                    # So if the run of '+' is short, then the input might be invalid or our logic is flawed.
                    # But given the constraints, let's assume it's valid.
                    # Actually, maybe the '+' at (r, c) is part of a border but not the top-left?
                    # No, because of the scanning order.
                    pass
                
                # Now find the bottom edge.
                # We need to find the lowest row r2 such that grid[r2][c] == '+' and grid[r2][c_right] == '+'
                # and all cells between r and r2 in columns c and c_right are '+'.
                # Also, the width must be at least 3.
                
                r2 = r
                while r2 + 1 < H:
                    # Check if the current row r2+1 has '+' at c and c_right
                    if grid[r2 + 1][c] == '+' and grid[r2 + 1][c_right] == '+':
                        # Check if the top and bottom borders are consistent so far
                        # Actually, we just need to ensure that the vertical borders are '+'
                        # But we also need to ensure that the horizontal borders at the ends are '+'
                        # Let's just extend as long as the corners are '+'
                        r2 += 1
                    else:
                        break
                
                # Now we have a candidate rectangle from (r, c) to (r2, c_right)
                # Check if it's valid:
                # 1. Width >= 3, Height >= 3
                # 2. All border cells are '+'
                # 3. No other '+' from another image touches this image (including corners)
                
                width = c_right - c + 1
                height = r2 - r + 1
                
                if width < 3 or height < 3:
                    # This shouldn't happen for a valid top-left corner
                    # But if it does, maybe this '+' is not a top-left corner?
                    # Let's skip it? But the problem says all '+' belong to exactly one image.
                    # So if we encounter a '+' and it's not visited, it must be a top-left.
                    # If the rectangle is too small, then the input is invalid? 
                    # Or maybe my assumption about top-left is wrong.
                    # Let's reconsider: 
                    # What if the image is:
                    # +++++
                    # +   +
                    # +   +
                    # +++++
                    # And we are at (0, 0). We find c_right=4, r2=3. Valid.
                    # What if we have:
                    # +++++
                    # +   +
                    # +   +
                    # +++++
                    # And we are at (0, 1)? We would have visited (0, 0) already.
                    # So yes, the first '+' we see is always top-left.
                    # So if width < 3 or height < 3, then the input is invalid or we made a mistake.
                    # Given the problem statement, we assume valid input.
                    # But to be safe, let's just skip if invalid.
                    continue
                
                # Check borders
                valid_image = True
                
                # Check top and bottom rows
                for col in range(c, c_right + 1):
                    if grid[r][col] != '+':
                        valid_image = False
                        break
                    if grid[r2][col] != '+':
                        valid_image = False
                        break
                
                if not valid_image:
                    continue
                
                # Check left and right columns
                for row in range(r, r2 + 1):
                    if grid[row][c] != '+':
                        valid_image = False
                        break
                    if grid[row][c_right] != '+':
                        valid_image = False
                        break
                
                if not valid_image:
                    continue
                
                # Check for adjacency with other images
                # The problem says borders of different images will not be adjacent.
                # This includes corners.
                # Since we are processing in order, we need to check if this new image touches any previously found image.
                # But the problem guarantees that borders are not adjacent.
                # So we don't need to check? 
                # Wait, the problem says "Borders of different images will not be adjacent to each other".
                # This is a guarantee on the input. So we don't need to check.
                # However, we need to make sure that we don't include '+' that belong to other images.
                # But since borders are not adjacent, the border of this image cannot touch the border of another image.
                # So we are safe.
                
                # Mark all '+' in this border as visited
                for col in range(c, c_right + 1):
                    visited_plus.add((r, col))
                    visited_plus.add((r2, col))
                for row in range(r, r2 + 1):
                    visited_plus.add((row, c))
                    visited_plus.add((row, c_right))
                
                images.append((r, c, r2, c_right))
    
    # Now we have all images.
    # We need to find banned characters inside images.
    # Banned characters are any character that is not in 'allowed'.
    # For every banned character found inside at least one image, the smallest image (in terms of pixel count) that contains that character will be flagged as an ad and removed.
    # When an ad is removed, every character inside the ad and the border is replaced with a whitespace.
    
    # Note: "inside at least one image" means the character is within the bounding box of an image (including border).
    # But the problem says "inside at least one image", and then "the smallest image ... that contains that character".
    # So we need to find all banned characters in the grid, and for each, find the smallest image that contains it.
    # Then mark that image for removal.
    
    # However, images can be nested.
    # If a character is in a nested image, it is also in the outer image.
    # We need to find the smallest image that contains the character.
    # The size of an image is (r2 - r + 1) * (c_right - c + 1).
    
    # Let's collect all banned characters and their positions.
    # Then for each banned character, find the smallest image that contains it.
    # Then mark those images for removal.
    
    # But wait, the problem says "For every banned character that is found inside at least one image".
    # So if a banned character is not inside any image, we ignore it.
    # How do we know if a character is inside an image?
    # A character at (r, c) is inside an image if r1 <= r <= r2 and c1 <= c <= c2 for some image (r1, c1, r2, c2).
    
    # Let's create a list of images with their sizes.
    image_list = []
    for (r1, c1, r2, c2) in images:
        size = (r2 - r1 + 1) * (c2 - c1 + 1)
        image_list.append({'r1': r1, 'c1': c1, 'r2': r2, 'c2': c2, 'size': size})
    
    # Sort images by size
    image_list.sort(key=lambda x: x['size'])
    
    # Now, find all banned characters and the smallest image containing them.
    # We can iterate over all cells, if the cell is inside any image and contains a banned character,
    # then find the smallest image that contains it.
    # But we need to be careful: if a character is in multiple images, we pick the smallest one.
    # And we mark that image for removal.
    
    # Let's create a set of images to remove.
    images_to_remove = set()
    
    # We can iterate over all images in increasing order of size.
    # For each image, check if it contains any banned character.
    # If it does, then this image is the smallest image containing those banned characters?
    # Not necessarily. A banned character might be in a smaller image that we haven't checked yet?
    # No, we are iterating in increasing order of size.
    # So if we find a banned character in the current image, and this image is the smallest one containing it,
    # then we mark it for removal.
    # But how do we know if it's the smallest?
    # We can check all images that contain the character and pick the smallest.
    # But that would be inefficient.
    # Alternatively, we can iterate over all cells, and for each banned character, find the smallest image containing it.
    # Since H, W <= 200, we can do this.
    
    # Let's create a 2D array to mark if a cell is inside an image.
    # But we need to know which image.
    # Actually, we can just iterate over all images, and for each image, check if it contains any banned character.
    # If it does, then this image is a candidate for removal.
    # But we need to ensure that we only remove the smallest image containing the banned character.
    # So, for each banned character, we find the smallest image containing it.
    # Then we add that image to the set of images to remove.
    
    # Let's do this:
    # Create a set of banned positions.
    banned_positions = set()
    for r in range(H):
        for c in range(W):
            if grid[r][c] not in allowed:
                # Check if this position is inside any image
                inside_any = False
                for img in image_list:
                    if img['r1'] <= r <= img['r2'] and img['c1'] <= c <= img['c2']:
                        inside_any = True
                        break
                if inside_any:
                    banned_positions.add((r, c))
    
    # Now, for each banned position, find the smallest image containing it.
    for (r, c) in banned_positions:
        min_size = float('inf')
        min_img = None
        for img in image_list:
            if img['r1'] <= r <= img['r2'] and img['c1'] <= c <= img['c2']:
                if img['size'] < min_size:
                    min_size = img['size']
                    min_img = img
        if min_img:
            images_to_remove.add((min_img['r1'], min_img['c1'], min_img['r2'], min_img['c2']))
    
    # Now, remove the images.
    # When an ad is removed, every character inside the ad and the border is replaced with a whitespace.
    # Note: "inside the ad and the border" means the entire rectangle of the image.
    
    for (r1, c1, r2, c2) in images_to_remove:
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                grid[r][c] = ' '
    
    # Output the grid
    for row in grid:
        print(row)

if __name__ == '__main__':
    solve()