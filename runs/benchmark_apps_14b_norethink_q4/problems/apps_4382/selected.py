import sys

def count_possible_passwords(N):
    return N ** 3

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    print(count_possible_passwords(N))