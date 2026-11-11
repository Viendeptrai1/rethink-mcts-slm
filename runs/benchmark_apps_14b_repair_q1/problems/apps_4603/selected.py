import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    D = int(data[3])
    
    min_train_fare = min(A, B)
    min_bus_fare = min(C, D)
    
    total_min_fare = min_train_fare + min_bus_fare
    
    print(total_min_fare)

if __name__ == "__main__":
    main()