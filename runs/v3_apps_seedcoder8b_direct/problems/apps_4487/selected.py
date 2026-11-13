def check_word_chain(A, B, C):
    if A[-1] == B[0] and B[-1] == C[0]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    A, B, C = data[0], data[1], data[2]
    check_word_chain(A, B, C)