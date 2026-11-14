import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        first_line = input_data[0].split()
        H, W = int(first_line[0]), int(first_line[1])
    except (ValueError, IndexError):
        return

    grid = []
    for i in range(1, H + 1):
        if i < len(input_data):
            grid.append(list(input_data[i]))
        else:
            grid.append([''] * W)

    # Allowed characters
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!,. ")
    border_char = '+'

    # Step 1: Detect all valid images
    # An image is a rectangle of '+' on the border, size at least 3x3.
    # We need to find all such rectangles.
    # Since borders cannot touch (not even corners), we can iterate and find top-left corners.
    
    images = []  # List of (r1, c1, r2, c2)
    
    # We scan for top-left corners of potential images.
    # A top-left corner must be a '+' and the 3x3 area starting there must be valid.
    # However, we must ensure that the '+' at (r, c) is not part of another image's border.
    # The problem states: "All '+' characters belong to the border of exactly 1 image."
    # This implies that if we find a '+' that is part of a valid image, it belongs to that image.
    # But we need to identify the images first.
    
    # Strategy:
    # 1. Identify all '+' positions.
    # 2. For each '+' that could be a top-left corner (i.e., not part of another image's border yet),
    #    try to expand to find the maximal rectangle of '+' that forms a valid image.
    #    But wait, the rule says borders don't touch. So if we find a '+' that is part of an image,
    #    we can determine the image boundaries.
    
    # Let's find all maximal rectangles of '+' that satisfy the image properties.
    # Since borders don't touch, each '+' belongs to exactly one image.
    # We can iterate through every cell. If it's a '+', and it hasn't been assigned to an image yet,
    # we try to find the image it belongs to.
    # Actually, simpler: Find all top-left corners of images.
    # A cell (r, c) is a top-left corner of an image if:
    #   - grid[r][c] == '+'
    #   - The 3x3 block starting at (r,c) has '+' at (r, c), (r, c+2), (r+2, c), (r+2, c+2) and the rest of the border is '+'
    #   - AND (r, c) is not part of any other image's border.
    # How to check if (r,c) is part of another image?
    #   - Check if there is a '+' at (r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)
    #     that could be part of another image.
    #   - Actually, the condition "borders of different images will not be adjacent" means no shared edges or corners.
    #   - So if (r,c) is a top-left, then (r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)
    #     cannot be '+' unless they are part of the SAME image (which is impossible for top-left relative to itself)
    #     or they are not part of any image.
    #   - Specifically, if (r,c) is top-left, then (r-1, c-1) cannot be '+', (r-1, c) cannot be '+', (r-1, c+1) cannot be '+',
    #     (r, c-1) cannot be '+', (r, c+1) cannot be '+', (r+1, c-1) cannot be '+', (r+1, c) cannot be '+', (r+1, c+1) cannot be '+'.
    #     Wait, (r+1, c+1) is inside the image, so it can be '+'. But (r+1, c+1) is not a border of the current image unless the image is 3x3.
    #     If the image is 3x3, the border includes (r+1, c+1).
    #     The rule "borders ... not adjacent" means the set of border cells of image A and set of border cells of image B are disjoint and not adjacent (8-connectivity).
    #     So if (r,c) is top-left of image A, then no cell in the 3x3 neighborhood of (r,c) except (r,c) itself can be a border cell of another image.
    #     But (r,c) is a border cell of A. So no other image can have a border cell in the 3x3 neighborhood of (r,c).
    #     This means we can simply check: if grid[r][c] == '+', and the 3x3 neighborhood (excluding (r,c) itself? No, including neighbors)
    #     does not contain any '+' that is part of a different image.
    #     But we don't know the images yet.
    
    # Alternative approach:
    # Since borders don't touch, we can find all connected components of '+'? No, because images are separate.
    # But images can be nested. Nested images share no border cells.
    # So all '+' cells form a set of disjoint components where each component is a single image?
    # No, because an image is a rectangle of '+'. The interior can contain anything.
    # But the border is all '+'.
    # If we have nested images, the inner image's border is inside the outer image's interior.
    # The outer image's border is a rectangle. The inner image's border is a smaller rectangle inside.
    # These two sets of '+' are disjoint.
    # So yes, all '+' cells in the grid belong to exactly one image, and no two images share a '+' cell.
    # Also, no two images have '+' cells adjacent (8-connectivity).
    # This means the '+' cells form a set of isolated clusters, where each cluster is exactly the border of one image.
    # Wait, if they are isolated (no adjacency), then we can just find connected components of '+' using 8-connectivity?
    # No, because the border of an image is connected via 4-connectivity (or 8-connectivity along the perimeter).
    # But the rule says borders are not adjacent. So the '+' cells of one image are not adjacent to '+' cells of another image.
    # Therefore, the '+' cells of one image form a connected component (in 4-connectivity or 8-connectivity) and are disjoint from other images.
    # So we can find all connected components of '+' cells. Each component corresponds to exactly one image.
    # Then we verify if each component forms a valid image (rectangle, size >= 3x3).
    
    # Let's do that.
    
    visited_plus = set()
    images = []
    
    for r in range(H):
        for c in range(W):
            if grid[r][c] == '+' and (r, c) not in visited_plus:
                # Found a new component of '+'
                component = []
                stack = [(r, c)]
                visited_plus.add((r, c))
                
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < H and 0 <= nc < W:
                                if grid[nr][nc] == '+' and (nr, nc) not in visited_plus:
                                    visited_plus.add((nr, nc))
                                    stack.append((nr, nc))
                
                # Now we have a component. Check if it forms a valid image.
                # It must be a rectangle border.
                # Find bounding box of the component.
                min_r = min(cr for cr, cc in component)
                max_r = max(cr for cr, cc in component)
                min_c = min(cc for cr, cc in component)
                max_c = max(cc for cr, cc in component)
                
                width = max_c - min_c + 1
                height = max_r - min_r + 1
                
                if width < 3 or height < 3:
                    # Not a valid image (too small)
                    # But wait, the problem says "All '+' characters belong to the border of exactly 1 image."
                    # This implies that if we find a '+' that is not part of a valid image, it's a contradiction?
                    # Or maybe the input guarantees that all '+' are part of valid images?
                    # "All '+' characters belong to the border of exactly 1 image."
                    # So we can assume every connected component of '+' is a valid image.
                    # But let's verify just in case.
                    # If it's not a valid image, then the input violates the condition.
                    # We'll assume valid input.
                    pass
                
                # Verify it is a rectangle border
                is_valid = True
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        if (r, c) in component:
                            # Should be on the border
                            if not (r == min_r or r == max_r or c == min_c or c == max_c):
                                is_valid = False
                                break
                        else:
                            # Should be '+' if on border, but we are checking if the component is exactly the border.
                            # If a cell on the border is not in the component, then the component is not the full border.
                            if r == min_r or r == max_r or c == min_c or c == max_c:
                                is_valid = False
                                break
                    if not is_valid:
                        break
                
                if is_valid:
                    images.append((min_r, min_c, max_r, max_c))
                else:
                    # This should not happen based on problem statement
                    # But if it does, we ignore it? Or treat as invalid?
                    # Given "All '+' characters belong to the border of exactly 1 image", we assume valid.
                    pass

    # Step 2: Find banned characters and determine which image to remove.
    # Banned characters: any char not in 'allowed' set.
    # For each banned char found inside an image, find the smallest image (by pixel count = area) that contains it.
    # Flag that image for removal.
    
    # Note: "inside at least one image" -> the character must be within the bounding box of an image.
    # Also, the character must be part of the image content (not the border? The problem says "inside at least one image").
    # Usually "inside" includes the border? But the border is '+', which is allowed.
    # Banned characters are not '+', so they won't be on the border.
    # So we just check if the banned char is within the bounding box of an image.
    
    # We need to map each banned char occurrence to the smallest image containing it.
    # Then mark that image for removal.
    
    images_to_remove = set()
    
    # Precompute area for each image
    image_areas = {}
    for i, (r1, c1, r2, c2) in enumerate(images):
        area = (r2 - r1 + 1) * (c2 - c1 + 1)
        image_areas[i] = area
    
    # Iterate over all cells
    for r in range(H):
        for c in range(W):
            char = grid[r][c]
            if char not in allowed:
                # Banned character
                # Find all images that contain this cell
                containing_images = []
                for i, (r1, c1, r2, c2) in enumerate(images):
                    if r1 <= r <= r2 and c1 <= c <= c2:
                        containing_images.append(i)
                
                if containing_images:
                    # Find the smallest image
                    min_idx = min(containing_images, key=lambda i: image_areas[i])
                    images_to_remove.add(min_idx)

    # Step 3: Remove flagged images
    # Replace all characters in the flagged images (including border) with whitespace.
    # We need to be careful: if an image is inside another, and the outer one is removed, the inner one is still there?
    # The problem says: "When an ad is removed, every character inside the ad and the border is replaced with a whitespace."
    # It doesn't say nested images are protected.
    # But if the outer image is removed, its content (including the inner image's border) becomes whitespace.
    # So the inner image is effectively destroyed.
    # This is consistent with "replace with whitespace".
    
    # So we just iterate over all flagged images and replace their bounding box with spaces.
    # Order doesn't matter because we are replacing with spaces, and spaces are allowed.
    # But wait, if we have overlapping images? The problem says borders don't touch, but images can be nested.
    # Nested images: outer image contains inner image.
    # If outer is removed, inner is gone.
    # If inner is removed, outer remains? Yes, unless outer is also flagged.
    # So we should process removals. But since we replace with spaces, the order of processing removals doesn't matter for the final result.
    # We just need to ensure that for each flagged image, we replace its entire bounding box with spaces.
    # However, if we have two flagged images, one inside another, and we replace the outer one first, the inner one's box is already spaces.
    # Then we replace the inner one's box (which is already spaces) with spaces. No problem.
    # If we replace the inner one first, then the outer one, the outer one's box includes the inner one's box, so we overwrite with spaces again.
    # So order doesn't matter.
    
    # But wait, what if an image is not flagged, but contains a flagged image?
    # The flagged image is removed (replaced with spaces). The outer image remains.
    # The outer image's content now has spaces where the inner image was.
    # This is correct.
    
    # So we just iterate over all flagged images and replace their bounding boxes with spaces.
    
    # However, we must be careful: if we replace the outer image first, the inner image's border becomes spaces.
    # Then when we try to replace the inner image, its bounding box is already spaces.
    # This is fine.
    
    # But what if the inner image is NOT flagged, but the outer image IS flagged?
    # Then we replace the outer image's box with spaces. The inner image is gone.
    # This is correct.
    
    # What if the inner image IS flagged, but the outer image is NOT?
    # Then we replace the inner image's box with spaces. The outer image remains, but with a hole (spaces) where the inner image was.
    # This is correct.
    
    # So the plan is solid.
    
    # One detail: "For every banned character that is found inside at least one image, in order not to remove too many unnecessary parts of the images on the web page, you decide that the smallest image (in terms of pixel count) that contains that character will be flagged as an ad and removed."
    # This means if a banned char is in multiple images, we only remove the smallest one.
    # We have already implemented this by taking the min index based on area.
    
    # Now, implement the removal.
    
    # We need to modify the grid.
    # Since we have the list of images, we can iterate and replace.
    # But note: if we have multiple images to remove, we should do it carefully.
    # Actually, since we are replacing with spaces, and spaces are allowed, we can just do it in any order.
    # However, to be safe, let's collect all flagged images and then process them.
    
    # But wait, what if an image is flagged, and we replace it with spaces.
    # Then another image (which was inside the first) is also flagged?
    # We already handled that: the inner image's box is a subset of the outer image's box.
    # So replacing the outer image's box with spaces will also replace the inner image's box.
    # So we don't need to worry about order.
    
    # Let's collect all flagged images.
    flagged_images = []
    for i in images_to_remove:
        flagged_images.append(images[i])
    
    # Now replace
    for (r1, c1, r2, c2) in flagged_images:
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                grid[r][c] = ' '
    
    # Output the result
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    solve()