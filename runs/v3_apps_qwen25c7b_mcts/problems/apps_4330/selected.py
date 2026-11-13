import sys

def find_k(A, B):
    if A > B:
        A, B = B, A
    if (B - A) % 2 == 0:
        return A + (B - A) // 2
    else:
        return "IMPOSSIBLE"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    result = find_k(A, B)
    print(result)