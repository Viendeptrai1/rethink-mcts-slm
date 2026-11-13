import sys

def count_passwords(N):
    return N ** 3

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = count_passwords(N)
    print(result)