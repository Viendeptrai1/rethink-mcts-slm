def find_longest_increasing_sequence(n, a):
    # Create a list to store whether each element is taken 'L' or 'R'
    sequence = [''] * n
    # Initialize pointers for the left and right ends
    left, right = 0, n - 1
    # Initialize the result length and pointer for the result sequence
    length = 0
    result_sequence = []

    # We need to create a strictly increasing sequence
    # Strategy: Use a greedy approach to take elements which can be part of an increasing sequence
    # Start with the smallest possible value which is always available as it appears exactly once
    current_value = 0
    while left <= right:
        if a[left] == current_value + 1:
            sequence[length] = 'L'
            current_value = a[left]
            left += 1
        elif a[right] == current_value + 1:
            sequence[length] = 'R'
            current_value = a[right]
            right -= 1
        else:
            # If neither end can be part of the increasing sequence, move both ends
            left += 1
            right -= 1
        length += 1

    # Print the result
    print(length)
    print(''.join(sequence[:length]))

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))
find_longest_increasing_sequence(n, a)