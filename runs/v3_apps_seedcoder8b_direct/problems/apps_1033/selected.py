def min_spots(n, H):
    # Start with the minimum number of spots required to satisfy the conditions
    # We need at least one spot to start with
    spots = 0
    remaining_sand = n

    # We need to ensure that the first spot's height is at least H
    # This means we need to use H packs of sand on the first spot
    if remaining_sand >= H:
        spots += 1
        remaining_sand -= H

    # Now we need to distribute the remaining sand in a way that satisfies the conditions
    # We can use a greedy approach to fill the spots
    while remaining_sand > 0:
        # We can either place a single sand pack or two adjacent spots with height difference of 1
        # We should try to place two adjacent spots with height difference of 1 if possible
        if remaining_sand >= 2:
            spots += 1
            remaining_sand -= 2
        else:
            spots += 1
            remaining_sand -= 1

    return spots

# Read input
import sys
input = sys.stdin.read
data = input().strip()
n, H = map(int, data.split())

# Calculate and print the result
print(min_spots(n, H))