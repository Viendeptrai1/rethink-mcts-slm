def find_earliest_abc(N):
    for x in range(N, 1000):
        if len(set(str(x))) == 1:
            return x

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    N = int(input().strip())
    print(find_earliest_abc(N))