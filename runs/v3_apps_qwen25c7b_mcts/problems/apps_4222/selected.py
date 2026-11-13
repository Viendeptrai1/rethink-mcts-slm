import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    snuke_has_snacks = [False] * (N + 1)
    
    for _ in range(K):
        d = int(data[index])
        index += 1
        for _ in range(d):
            snuke = int(data[index])
            index += 1
            snuke_has_snacks[snuke] = True
    
    victims = sum(1 for i in range(1, N + 1) if not snuke_has_snacks[i])
    
    print(victims)

if __name__ == "__main__":
    main()