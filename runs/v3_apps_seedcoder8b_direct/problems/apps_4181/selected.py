def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:N+2]))
    B = list(map(int, data[N+2:N+2+N]))
    
    total_monsters_defeated = 0
    
    for i in range(N):
        # Calculate the maximum monsters the i-th hero can defeat
        monsters_to_defeat = min(A[i] + A[i+1], B[i])
        total_monsters_defeated += monsters_to_defeat
        # Reduce the monsters in the towns by the number the hero defeats
        A[i] -= monsters_to_defeat // 2
        A[i+1] -= monsters_to_defeat - monsters_to_defeat // 2
    
    print(total_monsters_defeated)

if __name__ == "__main__":
    main()