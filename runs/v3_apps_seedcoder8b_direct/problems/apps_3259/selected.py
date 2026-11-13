def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    Q = int(data[index + 1])
    index += 2
    
    results = []
    
    for _ in range(Q):
        query_type = int(data[index])
        if query_type == 1:
            L = int(data[index + 1])
            R = int(data[index + 2])
            A = int(data[index + 3])
            B = int(data[index + 4])
            index += 5
            
            # Simulate the machine's operation
            for i in range(L, R + 1):
                # Calculate the number of stones for the i-th box
                stones = (i - L + 1) * A % B
                # Update the number of stones in the i-th box
                # (In a real scenario, we would update an array, but here we just simulate)
        
        elif query_type == 2:
            L = int(data[index + 1])
            R = int(data[index + 2])
            index += 3
            
            # Calculate the total number of stones in the range [L, R]
            total_stones = 0
            for i in range(L, R + 1):
                # Calculate the number of stones for the i-th box
                stones = (i - L + 1) * A % B
                total_stones += stones
            
            # Store the result for this query
            results.append(total_stones)
    
    # Print all results for queries of type 2
    for result in results:
        print(result)

if __name__ == "__main__":
    main()