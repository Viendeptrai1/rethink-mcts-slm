import sys

def max_increasing_subarray_length(n, a):
    if n == 1:
        return 1
    
    # Find the longest increasing subarray without any removal
    lis = [1] * n
    for i in range(1, n):
        if a[i] > a[i - 1]:
            lis[i] = lis[i - 1] + 1
    
    # Find the longest increasing subarray with one removal
    max_length = 0
    for i in range(n):
        left = lis[i - 1] if i > 0 else 0
        right = lis[i + 1] if i < n - 1 else 0
        max_length = max(max_length, left + right)
    
    return max_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = max_increasing_subarray_length(n, a)
    print(result)

if __name__ == "__main__":
    main()