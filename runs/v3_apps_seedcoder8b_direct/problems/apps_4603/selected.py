def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    D = int(data[3])
    
    # Calculate the minimum fare for trains
    train_fare = min(A, B)
    
    # Calculate the minimum fare for buses
    bus_fare = min(C, D)
    
    # Calculate the total minimum fare
    total_fare = train_fare + bus_fare
    
    # Print the result
    print(total_fare)

if __name__ == "__main__":
    main()