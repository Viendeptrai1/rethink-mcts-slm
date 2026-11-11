import sys

def find_k(A, B):
    if A == B:
        return "IMPOSSIBLE"
    K = (A + B) // 2
    if (A + B) % 2 == 0:
        return K
    else:
        return "IMPOSSIBLE"

def main():
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    result = find_k(A, B)
    print(result)

if __name__ == "__main__":
    main()