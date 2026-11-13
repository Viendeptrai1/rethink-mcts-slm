import sys

def find_largest_value(A, B):
    return max(A + B, A - B, A * B)

if __name__ == "__main__":
    A, B = map(int, sys.stdin.read().split())
    result = find_largest_value(A, B)
    print(result)