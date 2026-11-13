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

    # Construct the array to achieve this maximum minimum mex
    a = [0] * n
    current_value = 0
    for i in range(n):
        a[i] = current_value
        if mex_count[current_value] > 0:
            mex_count[current_value] -= 1
            current_value += 1

    # Output the result
    print(max_min_mex)
    print(' '.join(map(str, a)))

# Example usage:
# n, m = 5, 3
# subarrays = [(1, 3), (2, 5), (4, 5)]
# find_maximum_minimum_mex(n, m, subarrays)