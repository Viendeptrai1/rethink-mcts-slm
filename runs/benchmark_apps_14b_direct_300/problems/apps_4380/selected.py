import sys

def main():
    A, B = map(int, sys.stdin.read().split())
    
    # Check if both A and B are odd
    if A % 2 == 1 and B % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()