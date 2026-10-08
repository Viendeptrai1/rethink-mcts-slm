def longest_subarray_with_even_occurrences(arr):
    n = len(arr)
    if n == 0:
        return 0

    # Dictionary to store the first occurrence of each bitmask
    first_occurrence = {}
    # Bitmask to keep track of the parity of occurrences of each element
    bitmask = 0
    # Variable to store the maximum length of the sub-array
    max_length = 0

    for i in range(n):
        # Update the bitmask by toggling the bit corresponding to arr[i]
        bitmask ^= (1 << arr[i])

        # If the bitmask is 0, it means all elements have appeared an even number of times
        if bitmask == 0:
            max_length = i + 1
        else:
            # If this bitmask has been seen before, calculate the length of the sub-array
            if bitmask in first_occurrence:
                max_length = max(max_length, i - first_occurrence[bitmask])
            else:
                # Store the first occurrence of this bitmask
                first_occurrence[bitmask] = i

    return max_length

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
arr = list(map(int, data[1:]))

# Print the result
print(longest_subarray_with_even_occurrences(arr))