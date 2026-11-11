import sys

def max_erased_elements(n, a):
    if n == 1:
        return 0
    
    max_erase = 0
    
    # Check erasing from the start
    for i in range(1, n):
        if a[i] - a[i-1] > 1:
            max_erase = max(max_erase, i)
    
    # Check erasing from the end
    for i in range(n-2, -1, -1):
        if a[i+1] - a[i] > 1:
            max_erase = max(max_erase, n - i - 1)
    
    # Check erasing from the middle
    for i in range(1, n-1):
        if a[i+1] - a[i-1] > 2:
            max_erase = max(max_erase, i + (n - i - 2))
    
    return max_erase

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = max_erased_elements(n, a)
    print(result)

if __name__ == "__main__":
    main()