import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    snuke_has_snack = [False] * N
    
    for _ in range(K):
        d_i = int(data[index])
        index += 1
        for _ in range(d_i):
            A_ij = int(data[index]) - 1
            index += 1
            snuke_has_snack[A_ij] = True
    
    victims = sum(1 for has_snack in snuke_has_snack if not has_snack)
    print(victims)

if __name__ == "__main__":
    main()