import sys

def remaining_water_in_bottle_2():
    # Read input from standard input
    A, B, C = map(int, sys.stdin.readline().split())
    
    # Calculate the amount of water transferred
    transferred = min(A - B, C)
    
    # Calculate the remaining water in Bottle 2
    remaining = C - transferred
    
    # Print the result
    print(remaining)

# Call the function to execute
remaining_water_in_bottle_2()