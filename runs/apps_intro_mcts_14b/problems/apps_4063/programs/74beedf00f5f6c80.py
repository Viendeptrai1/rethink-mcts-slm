import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    difficulties.sort()
    
    count = 0
    for i in range(N // 2):
        if difficulties[i] < difficulties[N // 2]:
            count += 1
    
    print(count)

if __name__ == "__main__":
    main()