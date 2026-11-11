import sys

def main():
    input = sys.stdin.read().split()
    A = int(input[0])
    B = int(input[1])
    
    # Check if there exists a C such that A * B * C is odd
    if A % 2 == 1 and B % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()