import sys
import bisect

def main():
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

    # Current mex value
    current_mex = 0

    # Process each query in order of their right endpoint
    for l, r in queries:
        # Find the first position in the range [l-1, r-1] that is not yet assigned
        pos = bisect.bisect_left(a[l-1:r], current_mex)
        if pos < r - l + 1:
            # Assign the current mex to this position
            a[l-1+pos] = current_mex
            # Increment the current mex
            current_mex += 1

    # If there are still positions left unassigned, assign them arbitrary values
    for i in range(n):
        if a[i] == -1:
            a[i] = current_mex
            current_mex += 1

    # Output the result
    print(current_mex)
    print(' '.join(map(str, a)))

if __name__ == "__main__":
    main()