import sys

def count_triples(N, K):
    count = 0
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            for c in range(1, N + 1):
                if (a + b) % K == 0 and (b + c) % K == 0 and (c + a) % K == 0:
                    count += 1
    return count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    result = count_triples(N, K)
    print(result)