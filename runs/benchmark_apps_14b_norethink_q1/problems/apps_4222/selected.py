import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    snuke_set = set(range(1, N + 1))
    
    for _ in range(K):
        d_i = int(data[index])
        index += 1
        for _ in range(d_i):
            A_ij = int(data[index])
            index += 1
            if A_ij in snuke_set:
                snuke_set.remove(A_ij)
    
    print(len(snuke_set))

if __name__ == "__main__":
    main()