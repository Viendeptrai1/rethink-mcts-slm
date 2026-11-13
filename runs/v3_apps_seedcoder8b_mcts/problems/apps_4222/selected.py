def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    K = int(data[index])
    index += 1
    
    # Set to keep track of Snuke IDs who have at least one snack
    snukes_with_snacks = set()
    
    for _ in range(K):
        d_i = int(data[index])
        index += 1
        for _ in range(d_i):
            A_ij = int(data[index])
            index += 1
            snukes_with_snacks.add(A_ij)
    
    # Calculate the number of Snukes who have no snacks
    snukes_without_snacks = N - len(snukes_with_snacks)
    
    # Print the result
    print(snukes_without_snacks)

if __name__ == "__main__":
    main()