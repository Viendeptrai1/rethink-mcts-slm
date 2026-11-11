import sys
import heapq

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    n = data[0]
    a = data[1:]
    
    a.sort()
    
    min_instability = float('inf')
    
    # Consider removing the smallest element
    max_value = a[-1]
    min_value = a[1]
    min_instability = min(min_instability, max_value - min_value)
    
    # Consider removing the largest element
    max_value = a[-2]
    min_value = a[0]
    min_instability = min(min_instability, max_value - min_value)
    
    # Consider removing any other element
    for i in range(1, n - 1):
        max_value = max(a[i - 1], a[i + 1])
        min_value = min(a[i - 1], a[i + 1])
        min_instability = min(min_instability, max_value - min_value)
    
    print(min_instability)

if __name__ == "__main__":
    main()