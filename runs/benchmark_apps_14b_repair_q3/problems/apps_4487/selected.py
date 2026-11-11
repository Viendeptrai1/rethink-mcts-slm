import sys

def check_word_chain(A, B, C):
    if A[-1] == B[0] and B[-1] == C[0]:
        return "YES"
    else:
        return "NO"

if __name__ == "__main__":
    input = sys.stdin.read().strip().split()
    A, B, C = input[0], input[1], input[2]
    print(check_word_chain(A, B, C))