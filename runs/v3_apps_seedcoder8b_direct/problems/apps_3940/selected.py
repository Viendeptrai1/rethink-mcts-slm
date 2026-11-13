def find_maximum_minimum_mex(n, m, subarrays):
    from collections import defaultdict

    # Create a dictionary to count the frequency of each mex value
    mex_count = defaultdict(int)

    # Iterate over each subarray and calculate its mex
    for l, r in subarrays:
        present = set()
        mex = 0
        # Find the mex of the current subarray
        for i in range(l - 1, r):
            present.add(a[i])
            while mex in present:
                mex += 1
        # Increment the count of this mex value
        mex_count[mex] += 1

    # Find the maximum possible minimum mex
    max_min_mex = 0
    for mex in sorted(mex_count.keys()):
        if mex_count[mex] > 0:
            max_min_mex = mex

    # Construct the array a
    a = [0] * n
    current_value = 0
    for i in range(n):
        a[i] = current_value
        if i + 1 < n and current_value in [a[j] for j in range(i + 1)]:
            current_value += 1

    # Print the result
    print(max_min_mex)
    print(' '.join(map(str, a)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
subarrays = []
index = 2
for _ in range(m):
    l = int(data[index])
    r = int(data[index + 1])
    subarrays.append((l, r))
    index += 2

find_maximum_minimum_mex(n, m, subarrays)