def max_min_mex(n, m, queries):
    # Initialize the array with -1
    a = [-1] * n
    
    # Sort queries by length of subarray in descending order
    queries.sort(key=lambda x: x[1] - x[0], reverse=True)
    
    # Iterate over sorted queries
    for l, r in queries:
        # Find the smallest available number that is not in the current subarray
        mex = 0
        while True:
            if all(a[i] != mex for i in range(l-1, r)):
                break
            mex += 1
        
        # Assign the found mex value to the subarray
        for i in range(l-1, r):
            if a[i] == -1:
                a[i] = mex
                break
    
    # Return the maximum possible minimum mex and the array
    return max(a), a

# Read input
n, m = map(int, input().split())
queries = [tuple(map(int, input().split())) for _ in range(m)]

# Get result
result_mex, result_array = max_min_mex(n, m, queries)

# Print results
print(result_mex)
print(' '.join(map(str, result_array)))