def find_maximum_minimum_mex(n, m, queries):
    # To find the maximum possible minimum mex, we need to strategically place the values in the array.
    # We will distribute the mex values across the queries such that the smallest mex across all 
    # selected subarrays is maximized.

    # We will use a greedy approach:
    # 1. Start by sorting the queries based on the left index (l_i).
    # 2. Assign values to the array such that the mex condition is satisfied for each subarray.

    # Sort queries by left index
    queries.sort()

    # This will store the maximum mex we can achieve
    max_mex = 0

    # Initialize an array to store the result
    a = [0] * n

    # A dictionary to store the last used mex in the ranges
    last_used_mex = {}

    for l, r in queries:
        # Find the minimum mex that can be used for the current subarray
        # We need at least one number not in the current subarray, so we need to ensure
        # the mex is at least one more than the maximum of the range we've already covered.
        if (l, r) in last_used_mex:
            current_mex = last_used_mex[(l, r)]
        else:
            current_mex = max_mex

        # Fill the range with the current_mex
        for i in range(l - 1, r):
            a[i] = current_mex

        # Update the last used mex for this range
        last_used_mex[(l, r)] = current_mex + 1

        # Update the global max_mex
        max_mex = max(max_mex, current_mex + 1)

    # Output the result
    print(max_mex)
    print(*a)

import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    queries = []
    
    index = 2
    for _ in range(m):
        l = int(data[index])
        r = int(data[index + 1])
        queries.append((l, r))
        index += 2
    
    find_maximum_minimum_mex(n, m, queries)

if __name__ == "__main__":
    main()