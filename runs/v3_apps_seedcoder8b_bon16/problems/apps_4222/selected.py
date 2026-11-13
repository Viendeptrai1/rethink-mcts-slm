def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    # Read N and K
    idx = 0
    N = int(data[idx])
    K = int(data[idx + 1])
    idx += 2
    
    # Initialize a list to keep track of which Snukes have snacks
    snukes_with_snacks = [False] * (N + 1)
    
    # Process each kind of snack
    for _ in range(K):
        d_i = int(data[idx])
        idx += 1
        for j in range(d_i):
            snuke_index = int(data[idx])
            snukes_with_snacks[snuke_index] = True
            idx += 1
    
    # Count the number of Snukes without snacks
    victims = snukes_with_snacks[1:].count(False)
    
    # Print the result
    print(victims)

if __name__ == "__main__":
    main()