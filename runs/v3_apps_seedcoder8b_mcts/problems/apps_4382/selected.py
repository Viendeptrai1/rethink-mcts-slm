def count_passwords(N):
    return N * N * N

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    N = int(input().strip())
    print(count_passwords(N))