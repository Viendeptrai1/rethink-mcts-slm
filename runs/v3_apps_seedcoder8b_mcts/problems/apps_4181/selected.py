def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:N+2]))
    B = list(map(int, data[N+2:N+2+N]))
    
    def can_defeat(monsters, heroes):
        total_monsters = 0
        for i in range(len(heroes)):
            if i < len(monsters) - 1:
                total_monsters += min(heroes[i], monsters[i] + monsters[i + 1])
            else:
                total_monsters += min(heroes[i], monsters[i])
        return total_monsters
    
    print(can_defeat(A, B))

if __name__ == "__main__":
    main()