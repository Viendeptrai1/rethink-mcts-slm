def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    Q = int(data[index + 1])
    index += 2
    
    # Initialize an array to keep track of the number of stones in each box
    stones = [0] * (N + 1)
    
    # Process each query
    for _ in range(Q):
        if data[index] == '1':
            L = int(data[index + 1])
            R = int(data[index + 2])
            A = int(data[index + 3])
            B = int(data[index + 4])
            index += 5
            
            # Update the number of stones in the specified range
            for i in range(L, R + 1):
                stones[i] = ((i - L + 1) * A) % B
        elif data[index] == '2':
            L = int(data[index + 1])
            R = int(data[index + 2])
            index += 3
            
            # Calculate the total number of stones in the specified range
            total_stones = sum(stones[L:R + 1])
            print(total_stones)

if __name__ == "__main__":
    main()