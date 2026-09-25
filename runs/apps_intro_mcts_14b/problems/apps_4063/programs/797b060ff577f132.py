import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    difficulties.sort()
    
    target_count = N // 2
    arc_count = 0
    result = 0
    
    for i in range(N):
        if difficulties[i] >= difficulties[target_count - 1]:
            arc_count += 1
        if arc_count == target_count:
            result += 1
    
    print(result)

if __name__ == "__main__":
    main()