import sys

def main():
    import sys
    import bisect
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    n = data[0]
    a = data[1:]
    
    a.sort()
    
    min_instability = float('inf')
    
    for i in range(n):
        if i == 0:
            instability = a[n-1] - a[1]
        elif i == n-1:
            instability = a[n-2] - a[0]
        else:
            instability = min(a[i-1] - a[0], a[n-1] - a[i+1])
        
        min_instability = min(min_instability, instability)
    
    print(min_instability)

if __name__ == "__main__":
    main()