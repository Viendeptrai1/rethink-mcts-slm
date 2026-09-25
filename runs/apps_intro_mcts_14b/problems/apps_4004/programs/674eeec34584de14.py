import sys

def find_minimum_D(n, a):
    a.sort()
    median = a[n // 2]
    min_D = float('inf')
    
    for i in range(n):
        if a[i] == median:
            continue
        diff = abs(a[i] - median)
        if diff % 2 == 0:
            min_D = min(min_D, diff // 2)
        else:
            return -1
    
    return min_D if min_D != float('inf') else -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = find_minimum_D(n, a)
    print(result)

if __name__ == "__main__":
    main()