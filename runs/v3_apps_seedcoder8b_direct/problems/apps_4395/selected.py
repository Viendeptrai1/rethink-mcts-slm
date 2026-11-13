def make_garland_nice(n, s):
    # Helper function to calculate the minimum recolors needed for a given pattern
    def min_recolor_needed(pattern):
        recolor_count = 0
        for i in range(n):
            if s[i] != pattern[i % 3]:
                recolor_count += 1
        return recolor_count

    # Possible patterns for a nice garland
    patterns = ["RGB", "RBG", "GRB", "GBR", "BRG", "BGR"]

    # Initialize the minimum recolor count and the best pattern
    min_recolors = float('inf')
    best_pattern = ""

    # Check each pattern to find the one with the minimum recolor count
    for pattern in patterns:
        recolor_count = min_recolor_needed(pattern)
        if recolor_count < min_recolors:
            min_recolors = recolor_count
            best_pattern = pattern

    # Construct the resulting garland using the best pattern
    result_garland = ''.join(best_pattern[i % 3] for i in range(n))

    # Output the result
    print(min_recolors)
    print(result_garland)

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Call the function with the input data
make_garland_nice(n, s)