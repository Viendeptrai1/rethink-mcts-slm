import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    snuke_snacks = [set() for _ in range(N)]
    
    for _ in range(K):
        d_i = int(data[index])
        index += 1
        for j in range(d_i):
            A_ij = int(data[index]) - 1
            index += 1
            snuke_snacks[A_ij].add(j)
    
    victims = sum(1 for snacks in snuke_snacks if len(snacks) == 0)
    
    print(victims)

if __name__ == "__main__":
    main()