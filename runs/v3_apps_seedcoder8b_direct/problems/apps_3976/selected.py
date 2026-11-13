def find_valid_qs(n, m, p, a, b):
    from collections import Counter

    # Count the frequency of each element in sequence b
    b_count = Counter(b)

    # Initialize a list to store valid q values
    valid_qs = []

    # Iterate over possible starting points q
    for q in range(1, n - m * p + 2):
        # Create a counter for the current window in sequence a
        current_window = Counter(a[q - 1:q - 1 + m * p:p])

        # Check if the current window can be rearranged to match b
        if current_window == b_count:
            valid_qs.append(q)

    # Print the number of valid qs
    print(len(valid_qs))

    # Print the valid qs in increasing order
    if valid_qs:
        print(" ".join(map(str, valid_qs)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
m = int(data[1])
p = int(data[2])
a = list(map(int, data[3:3 + n]))
b = list(map(int, data[3 + n:3 + n + m]))

# Call the function with the parsed input
find_valid_qs(n, m, p, a, b)