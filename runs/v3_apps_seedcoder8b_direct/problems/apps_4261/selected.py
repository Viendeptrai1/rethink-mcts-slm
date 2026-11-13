def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B, C = map(int, data.split())
    
    # Calculate the maximum amount of water that can be transferred from Bottle 2 to Bottle 1
    transfer_amount = min(C, A - B)
    
    # Calculate the remaining water in Bottle 2
    remaining_water = C - transfer_amount
    
    # Print the result
    print(remaining_water)

if __name__ == "__main__":
    main()