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
        # Find the first position in the range [l-1, r-1] that is still -1
        pos = bisect.bisect_left(a, -1, l-1, r)
        
        if pos < r:
            # Assign the current mex value to this position
            a[pos] = current_mex
            # Increment the current mex value
            current_mex += 1

    # If there are still -1s in the array, assign the current mex value to them
    for i in range(n):
        if a[i] == -1:
            a[i] = current_mex
            current_mex += 1

    # Output the result
    print(current_mex)
    print(' '.join(map(str, a)))

if __name__ == "__main__":
    main()