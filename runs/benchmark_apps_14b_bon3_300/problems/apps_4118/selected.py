import sys

def main():
    # Read input from standard input
    A, B = map(int, sys.stdin.readline().split())
    
    # Check if Takahashi can calculate A * B
    if 1 <= A <= 9 and 1 <= B <= 9:
        print(A * B)
    else:
        print(-1)

if __name__ == "__main__":
    main()