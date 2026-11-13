def max_balanced_circle(n, heights):
    from collections import defaultdict

    # Count the frequency of each height
    height_count = defaultdict(int)
    for height in heights:
        height_count[height] += 1

    # Sort the unique heights
    unique_heights = sorted(height_count.keys())

    # Initialize variables to track the maximum balanced circle
    max_length = 0
    best_start = 0

    # Iterate over each unique height as a potential starting point
    for start in unique_heights:
        current_length = 0
        current_height = start

        # Try to build a balanced circle starting from this height
        while current_height in height_count:
            current_length += height_count[current_height]
            height_count[current_height] = 0  # Mark as used

            # Move to the next possible height
            if current_height + 1 in height_count:
                current_height += 1
            else:
                break

        # Check if this is the best circle found so far
        if current_length > max_length:
            max_length = current_length
            best_start = start

    # Reconstruct the best balanced circle
    result = []
    current_height = best_start
    while current_height in height_count:
        count = height_count[current_height]
        result.extend([current_height] * count)
        height_count[current_height] = 0  # Mark as used

        # Move to the next possible height
        if current_height + 1 in height_count:
            current_height += 1
        else:
            break

    # Output the result
    print(max_length)
    print(' '.join(map(str, result)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
heights = list(map(int, data[1:n+1]))

# Call the function with the input data
max_balanced_circle(n, heights)