import sys

def max_value(A, B):
    return max(A + B, A - B, A * B)

if __name__ == "__main__":
    A, B = map(int, sys.stdin.readline().split())
    print(max_value(A, B))