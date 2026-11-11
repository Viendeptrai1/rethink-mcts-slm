def find_valid_positions(n, m, p, a, b):
    # Sort the sequence b
    b_sorted = sorted(b)
    
    valid_positions = []
    
    # Iterate through possible starting positions q
    for q in range(1, n - (m - 1) * p + 1):
        # Extract the subsequence from a starting at q and incrementing by p
        subsequence = [a[q - 1 + i * p] for i in range(m)]
        
        # Check if the subsequence matches the sorted sequence b
        if sorted(subsequence) == b_sorted:
            valid_positions.append(q)
    
    # Output the number of valid positions and the positions themselves
    print(len(valid_positions))
    print(' '.join(map(str, valid_positions)))

# Read input
n, m, p = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Find and print valid positions
find_valid_positions(n, m, p, a, b)