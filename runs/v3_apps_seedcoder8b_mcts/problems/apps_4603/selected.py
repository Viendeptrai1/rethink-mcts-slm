def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    D = int(data[3])
    
    min_fare = min(A, B) + min(C, D)
    print(min_fare)

if __name__ == "__main__":
    main()