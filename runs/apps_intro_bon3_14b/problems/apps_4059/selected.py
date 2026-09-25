import sys

def count_tuples(N):
    count = 0
    for A in range(1, N):
        for B in range(1, N // A + 1):
            C = N - A * B
            if C > 0:
                count += 1
    return count

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = count_tuples(N)
    sys.stdout.write(str(result))