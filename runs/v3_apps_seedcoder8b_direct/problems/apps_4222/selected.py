def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    K = int(data[index])
    index += 1
    
    # List to track which Snukes have snacks
    snukes_with_snacks = [False] * (N + 1)
    
    for _ in range(K):
        d_i = int(data[index])
        index += 1
        for _ in range(d_i):
            A_i_j = int(data[index])
            index += 1
            snukes_with_snacks[A_i_j] = True
    
    # Count Snukes without snacks
    victims = snukes_with_snacks.count(False) - 1  # Subtract 1 to exclude the 0th index
    
    print(victims)

if __name__ == "__main__":
    main()