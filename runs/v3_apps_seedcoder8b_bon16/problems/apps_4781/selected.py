def solve():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    K = int(data[0]) - 1  # Convert to 0-based index
    N = int(data[1])
    players = list(range(8))
    
    for i in range(2, 2 + N):
        T, Z = data[i].split()
        if Z == 'T':
            K = (K + 1) % 8
        elif Z == 'N' or Z == 'P':
            K = K  # The box stays with the same player
    
    print(players[K] + 1)