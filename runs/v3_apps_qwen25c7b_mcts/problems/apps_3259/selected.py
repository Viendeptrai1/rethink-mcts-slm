def simulate_queries(N, Q, queries):
    boxes = [0] * (N + 1)
    results = []

    for query in queries:
        if query[0] == 1:
            L, R, A, B = query[1], query[2], query[3], query[4]
            for i in range(L, R + 1):
                boxes[i] = ((i - L + 1) * A) % B
        elif query[0] == 2:
            L, R = query[1], query[2]
            result = sum(boxes[L:R + 1])
            results.append(result)

    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
Q = int(data[1])

queries = []
index = 2
for _ in range(Q):
    query_type = int(data[index])
    if query_type == 1:
        L = int(data[index + 1])
        R = int(data[index + 2])
        A = int(data[index + 3])
        B = int(data[index + 4])
        queries.append((query_type, L, R, A, B))
        index += 5
    elif query_type == 2:
        L = int(data[index + 1])
        R = int(data[index + 2])
        queries.append((query_type, L, R))
        index += 3

# Process queries and print results
results = simulate_queries(N, Q, queries)
for result in results:
    print(result)