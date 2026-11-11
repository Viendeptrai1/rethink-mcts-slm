import sys

def max_elements_to_erase(n, a):
    if n == 1:
        return 0
    
    max_gap = 0
    for i in range(1, n):
        gap = a[i] - a[i-1] - 1
        max_gap = max(max_gap, gap)
    
    return max_gap

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = max_elements_to_erase(n, a)
    print(result)

if __name__ == "__main__":
    main()