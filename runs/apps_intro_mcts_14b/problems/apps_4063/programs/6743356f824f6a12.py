import sys
from bisect import bisect_left

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    difficulties.sort()
    
    target_count = N // 2
    valid_K_count = 0
    
    for i in range(N):
        if i == 0 or difficulties[i] != difficulties[i - 1]:
            count = N - bisect_left(difficulties, difficulties[i])
            if count == target_count:
                valid_K_count += 1
    
    print(valid_K_count)

if __name__ == "__main__":
    main()