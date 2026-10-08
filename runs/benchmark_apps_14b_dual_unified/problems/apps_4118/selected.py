import sys

def main():
    # Read input from standard input
    A, B = map(int, sys.stdin.read().split())
    
    # Check if both A and B are within the range of 1 to 9
    if 1 <= A <= 9 and 1 <= B <= 9:
        # Calculate and print the result
        print(A * B)
    else:
        # Print -1 if the condition is not met
        print(-1)

if __name__ == "__main__":
    main()