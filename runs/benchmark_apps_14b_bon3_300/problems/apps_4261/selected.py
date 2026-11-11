import sys

def main():
    # Read input from standard input
    A, B, C = map(int, sys.stdin.read().split())
    
    # Calculate how much water can be transferred from Bottle 2 to Bottle 1
    transfer_amount = min(C, A - B)
    
    # Calculate the remaining water in Bottle 2
    remaining_water_in_bottle2 = C - transfer_amount
    
    # Print the result
    print(remaining_water_in_bottle2)

if __name__ == "__main__":
    main()