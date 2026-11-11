import sys

def main():
    # Read input from standard input
    A, B, C = map(int, sys.stdin.read().split())
    
    # Calculate the maximum amount of water that can be transferred
    max_transfer = A - B
    
    # Determine the actual amount of water transferred
    actual_transfer = min(max_transfer, C)
    
    # Calculate the remaining water in Bottle 2
    remaining_water = C - actual_transfer
    
    # Print the result
    print(remaining_water)

if __name__ == "__main__":
    main()