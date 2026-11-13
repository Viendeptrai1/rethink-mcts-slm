def min_spots_to_build_castle(n, H):
    # Initialize the number of spots and the remaining sand packs
    spots = 0
    remaining_sand = n

    # Start placing pillars from the leftmost spot
    while remaining_sand > 0:
        # Determine the height of the current pillar
        if spots < H:
            # If we are within the height limit of the fence, place a pillar of height spots + 1
            height = spots + 1
        else:
            # If we have reached the height limit, place a pillar of height H
            height = H

        # Place the pillar and update the remaining sand packs
        remaining_sand -= height
        spots += 1

    return spots

# Read input
import sys
input = sys.stdin.read
data = input().strip()
n, H = map(int, data.split())

# Calculate and print the result
result = min_spots_to_build_castle(n, H)
print(result)