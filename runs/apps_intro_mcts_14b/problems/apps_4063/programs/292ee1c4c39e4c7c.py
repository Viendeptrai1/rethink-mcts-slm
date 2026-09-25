import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    difficulties.sort()
    
    target_count = N // 2
    count = 0
    
    for i in range(N):
        if difficulties[i] >= difficulties[target_count]:
            count += 1
    
    print(count)

if __name__ == "__main__":
    main()