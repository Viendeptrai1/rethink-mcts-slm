def max_min_mex(n, m, queries):
    # Initialize the array with zeros
    a = [0] * n
    
    # Sort queries by their length in descending order
    queries.sort(key=lambda x: x[1] - x[0], reverse=True)
    
    # Set the current mex value
    mex = 0
    
    # Process each query
    for l, r in queries:
        # Fill the array with the current mex value in the range [l-1, r-1]
        for i in range(l-1, r):
            if a[i] == 0:
                a[i] = mex
                mex += 1
                break
    
    # Return the maximum possible minimum mex and the array
    return mex, a

# Read input
import sys
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

# Get the result
result_mex, result_array = max_min_mex(n, m, queries)

# Print the result
print(result_mex)
print(' '.join(map(str, result_array)))