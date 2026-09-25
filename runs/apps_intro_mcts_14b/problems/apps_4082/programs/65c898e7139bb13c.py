import sys

def max_increasing_subarray_length(n, a):
    # Calculate the length of the longest increasing subarray ending at each position
    lis = [1] * n
    for i in range(1, n):
        if a[i] > a[i - 1]:
            lis[i] = lis[i - 1] + 1

    # Calculate the length of the longest increasing subarray starting at each position
    lds = [1] * n
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            lds[i] = lds[i + 1] + 1

    # Calculate the maximum length of the increasing subarray after removing one element
    max_length = 0
    for i in range(n):
        # If we remove the element at position i
        if i == 0:
            max_length = max(max_length, lds[i + 1])
        elif i == n - 1:
            max_length = max(max_length, lis[i - 1])
        else:
            max_length = max(max_length, lis[i - 1] + lds[i + 1])

    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_increasing_subarray_length(n, a))