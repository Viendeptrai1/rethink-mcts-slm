def simulate_device(N, Q, queries):
    boxes = [0] * (N + 1)
    
    def process_command(L, R, A, B):
        for X in range(L, R + 1):
            boxes[X] = ((X - L + 1) * A) % B
    
    def get_total_stones(L, R):
        return sum(boxes[L:R + 1])
    
    results = []
    for query in queries:
        if query[0] == 1:
            _, L, R, A, B = query
            process_command(L, R, A, B)
        elif query[0] == 2:
            _, L, R = query
            results.append(get_total_stones(L, R))
    
    return results

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    Q = int(data[1])
    queries = []
    index = 2
    for _ in range(Q):
        command = int(data[index])
        if command == 1:
            L = int(data[index + 1])
            R = int(data[index + 2])
            A = int(data[index + 3])
            B = int(data[index + 4])
            queries.append((command, L, R, A, B))
            index += 5
        elif command == 2:
            L = int(data[index + 1])
            R = int(data[index + 2])
            queries.append((command, L, R))
            index += 3
    
    results = simulate_device(N, Q, queries)
    for result in results:
        print(result)