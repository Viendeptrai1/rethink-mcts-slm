import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    has_snack = [False] * N
    
    for _ in range(K):
        d_i = int(data[index])
        index += 1
        for _ in range(d_i):
            A_i_j = int(data[index]) - 1
            index += 1
            has_snack[A_i_j] = True
    
    victims = sum(1 for snuke in has_snack if not snuke)
    print(victims)

if __name__ == "__main__":
    main()