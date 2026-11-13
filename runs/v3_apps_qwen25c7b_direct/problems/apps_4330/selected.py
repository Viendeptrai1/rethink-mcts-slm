import sys

def find_k(A, B):
    if A == B:
        return "IMPOSSIBLE"
    else:
        K = (A + B) // 2
        return K

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    result = find_k(A, B)
    print(result)