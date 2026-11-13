import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    snuck_has_snacks = set()
    
    for _ in range(K):
        di = int(data[index])
        index += 1
        for _ in range(di):
            ai = int(data[index]) - 1
            snuck_has_snacks.add(ai)
            index += 1
    
    total_snucks = set(range(N))
    victims = total_snucks - snuck_has_snacks
    
    print(len(victims))

if __name__ == "__main__":
    main()