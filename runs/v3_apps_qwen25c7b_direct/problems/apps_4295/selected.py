import sys

def min_possible_value(N, K):
    return abs(N % (2 * K))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    result = min_possible_value(N, K)
    print(result)