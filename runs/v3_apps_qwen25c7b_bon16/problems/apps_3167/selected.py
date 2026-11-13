from sys import stdin, stdout

def process_queries(N, K, jumps, Q, queries):
    # Initialize the array with zeros
    seq = [0] * N
    
    # Apply the jumps to the array
    for jump in jumps:
        i = 0
        while i < N:
            seq[i] += 1
            i += jump
    
    # Calculate the prefix sums for efficient query processing
    prefix_sums = [0]
    for value in seq:
        prefix_sums.append(prefix_sums[-1] + value)
    
    # Process each query
    results = []
    for L, R in queries:
        results.append(prefix_sums[R + 1] - prefix_sums[L])
    
    return results

# Read input
N, K = map(int, stdin.readline().split())
jumps = list(map(int, stdin.readline().split()))
Q = int(stdin.readline().split()[0])
queries = [tuple(map(int, stdin.readline().split())) for _ in range(Q)]

# Get the results
results = process_queries(N, K, jumps, Q, queries)

# Print results
for result in results:
    stdout.write(f"{result}\n")