import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    jumps = list(map(int, data[index:index + K]))
    index += K
    
    Q = int(data[index])
    index += 1
    
    queries = []
    for _ in range(Q):
        L = int(data[index])
        R = int(data[index + 1])
        queries.append((L, R))
        index += 2
    
    seq = [0] * N
    
    for jump in jumps:
        i = 0
        while i < N:
            seq[i] += 1
            i += jump
    
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i + 1] = prefix_sum[i] + seq[i]
    
    for L, R in queries:
        print(prefix_sum[R + 1] - prefix_sum[L])

if __name__ == "__main__":
    main()