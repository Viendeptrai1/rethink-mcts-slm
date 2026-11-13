def max_balanced_circle(n, heights):
    from collections import defaultdict

    # Count the frequency of each height
    height_count = defaultdict(int)
    for height in heights:
        height_count[height] += 1

    # Sort the unique heights
    unique_heights = sorted(height_count.keys())

    # Initialize variables to track the maximum circle
    max_circle = []
    max_circle_size = 0

    # Try to form a circle starting from each unique height
    for start_height in unique_heights:
        current_circle = []
        current_size = 0
        current_height = start_height

        # Try to add people to the circle
        while height_count[current_height] > 0:
            current_circle.append(current_height)
            height_count[current_height] -= 1
            current_size += 1

            # Move to the next possible height
            if height_count[current_height + 1] > 0:
                current_height += 1
            elif height_count[current_height - 1] > 0:
                current_height -= 1
            else:
                break

        # Check if this circle is the largest found
        if current_size > max_circle_size:
            max_circle_size = current_size
            max_circle = current_circle

    # Output the result
    print(max_circle_size)
    print(' '.join(map(str, max_circle)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
heights = list(map(int, data[1:]))

# Call the function with the input data
max_balanced_circle(n, heights)