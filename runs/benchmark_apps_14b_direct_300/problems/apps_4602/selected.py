import sys

def main():
    import sys
    import itertools

    def read_ints():
        return list(map(int, sys.stdin.read().split()))

    data = read_ints()
    N = data[0]
    K = data[1]
    x = data[2:]

    min_distance = float('inf')

    for assignment in itertools.product([0, 1], repeat=N):
        total_distance = 0
        for i in range(N):
            if assignment[i] == 0:
                total_distance += abs(x[i] - 0) + abs(x[i] - 0)
            else:
                total_distance += abs(x[i] - K) + abs(x[i] - K)
        min_distance = min(min_distance, total_distance)

    print(min_distance)

if __name__ == "__main__":
    main()