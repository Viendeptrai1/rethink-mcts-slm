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
    input = sys.stdin.read().split()
    A = int(input[0])
    B = int(input[1])
    result = find_k(A, B)
    print(result)

if __name__ == "__main__":
    main()