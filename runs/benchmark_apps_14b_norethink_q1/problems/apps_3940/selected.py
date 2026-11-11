import sys
import bisect

def solve():
    import sys
    import bisect

    def readints():
        return list(map(int, sys.stdin.readline().split()))

    n, m = readints()
    queries = [readints() for _ in range(m)]

    # Sort queries by their right endpoint
    queries.sort(key=lambda x: x[1])

    # Initialize the array with -1
    a = [-1] * n

    # Process each query in the sorted order
    for l, r in queries:
        # Find the smallest mex for the current subarray
        mex = 0
        while mex in a[l-1:r]:
            mex += 1

        # Assign the mex value to the rightmost position in the current subarray
        a[r-1] = mex

    # Ensure all elements are between 0 and 10^9
    for i in range(n):
        if a[i] == -1:
            a[i] = 0

    # Find the minimum mex among all subarrays
    min_mex = float('inf')
    for l, r in queries:
        subarray = a[l-1:r]
        mex = 0
        while mex in subarray:
            mex += 1
        min_mex = min(min_mex, mex)

    print(min_mex)
    print(' '.join(map(str, a)))

if __name__ == "__main__":
    solve()