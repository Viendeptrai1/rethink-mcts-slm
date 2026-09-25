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
    last_k = -1
    
    for i in range(N):
        if difficulties[i] > last_k:
            if N - i == target_count:
                count += 1
            last_k = difficulties[i]
    
    print(count)

if __name__ == "__main__":
    main()