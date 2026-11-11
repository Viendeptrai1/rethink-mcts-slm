import sys

def main():
    input = sys.stdin.read().strip().split()
    A, B, C = input[0], input[1], input[2]
    
    if A[-1] == B[0] and B[-1] == C[0]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()