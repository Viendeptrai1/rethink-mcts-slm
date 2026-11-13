def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B, C = map(int, data.split())
    
    # Transfer water from Bottle 2 to Bottle 1
    while B < A and C > 0:
        transfer_amount = min(A - B, C)
        B += transfer_amount
        C -= transfer_amount
    
    # Print the remaining amount of water in Bottle 2
    print(C)

if __name__ == "__main__":
    main()