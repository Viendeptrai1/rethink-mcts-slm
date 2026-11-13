def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    Q = int(data[index + 1])
    index += 2
    
    # To store the number of stones in each box
    stones = [0] * (N + 1)
    
    # To store the results of the operations
    results = [0] * (N + 1)
    
    for _ in range(Q):
        query_type = int(data[index])
        if query_type == 1:
            L = int(data[index + 1])
            R = int(data[index + 2])
            A = int(data[index + 3])
            B = int(data[index + 4])
            index += 5
            
            # Perform the operation and store the results
            for i in range(L, R + 1):
                stones[i] = ((i - L + 1) * A) % B
                results[i] += stones[i]
        
        elif query_type == 2:
            L = int(data[index + 1])
            R = int(data[index + 2])
            index += 3
            
            # Calculate the total number of stones in the range [L, R]
            total_stones = sum(results[L:R + 1])
            print(total_stones)

if __name__ == "__main__":
    main()