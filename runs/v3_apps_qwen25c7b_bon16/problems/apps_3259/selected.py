def simulate_device(N, Q):
    boxes = [0] * (N + 1)
    results = []

    for _ in range(Q):
        query = input().split()
        if query[0] == '1':
            L, R, A, B = map(int, query[1:])
            for X in range(L, R + 1):
                boxes[X] = ((X - L + 1) * A) % B
        elif query[0] == '2':
            L, R = map(int, query[1:])
            total_stones = sum(boxes[L:R + 1])
            results.append(total_stones)

    for result in results:
        print(result)

# Read input
N, Q = map(int, input().split())
simulate_device(N, Q)