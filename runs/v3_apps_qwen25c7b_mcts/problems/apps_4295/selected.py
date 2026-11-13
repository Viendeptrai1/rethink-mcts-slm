import sys

def min_value_after_operations(N, K):
    return max(0, (N + K - 1) // K * K - N)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    result = min_value_after_operations(N, K)
    print(result)