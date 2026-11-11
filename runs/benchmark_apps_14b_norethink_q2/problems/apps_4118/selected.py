import sys

def main():
    # Read input from standard input
    input = sys.stdin.read().strip().split()
    A = int(input[0])
    B = int(input[1])
    
    # Check if both A and B are within the range 1 to 9
    if 1 <= A <= 9 and 1 <= B <= 9:
        # Compute the product
        result = A * B
        print(result)
    else:
        # Print -1 if the condition is not met
        print(-1)

if __name__ == "__main__":
    main()