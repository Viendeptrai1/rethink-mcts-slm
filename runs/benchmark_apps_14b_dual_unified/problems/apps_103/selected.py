import sys

def max_consecutive_erasure(n, a):
    # Check if we can erase elements from the start
    start = 0
    while start + 1 < n and a[start + 1] - a[start] == 1:
        start += 1
    
    # Check if we can erase elements from the end
    end = n - 1
    while end > 0 and a[end] - a[end - 1] == 1:
        end -= 1
    
    # The maximum number of consecutive elements that can be erased
    return max(start, n - 1 - end)

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