def count_triples(N, K):
    count = 0
    for a in range(1, N + 1):
        if a % K == 0:
            for b in range(1, N + 1):
                if b % K == 0:
                    c = (a + b) % K
                    if c == 0:
                        count += N // K
                    elif c + K <= N:
                        count += (N - c) // K
    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, K = map(int, data.split())
    print(count_triples(N, K))