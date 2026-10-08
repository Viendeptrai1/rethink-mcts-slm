import sys

def main():
    # Read input from standard input
    A, B, C = map(int, sys.stdin.read().split())
    
    # Calculate the remaining capacity of Bottle 1
    remaining_capacity = A - B
    
    # Determine how much water can be transferred from Bottle 2 to Bottle 1
    water_transferred = min(remaining_capacity, C)
    
    # Calculate the remaining water in Bottle 2
    remaining_water_in_bottle_2 = C - water_transferred
    
    # Print the result
    print(remaining_water_in_bottle_2)

if __name__ == "__main__":
    main()