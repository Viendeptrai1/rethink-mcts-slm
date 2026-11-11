import sys

def max_consecutive_erasure(n, a):
    if n == 1:
        return 0
    
    max_erase = 0
    
    # Check erasing from the start
    if a[1] - a[0] > 1:
        max_erase = max(max_erase, a[1] - a[0] - 1)
    
    # Check erasing from the end
    if a[n-1] - a[n-2] > 1:
        max_erase = max(max_erase, a[n-1] - a[n-2] - 1)
    
    # Check erasing in the middle
    for i in range(1, n-1):
        if a[i+1] - a[i] > 1:
            max_erase = max(max_erase, a[i+1] - a[i] - 1)
    
    return max_erase

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    result = max_consecutive_erasure(n, a)
    print(result)

if __name__ == "__main__":
    main()