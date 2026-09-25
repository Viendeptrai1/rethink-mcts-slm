import sys
from collections import defaultdict

def count_median_pairs(n, m, a):
    # Create a prefix sum array for elements less than m
    less = [0] * (n + 1)
    # Create a prefix sum array for elements greater than m
    more = [0] * (n + 1)
    
    for i in range(n):
        if a[i] < m:
            less[i + 1] = less[i] + 1
        else:
            less[i + 1] = less[i]
        
        if a[i] > m:
            more[i + 1] = more[i] + 1
        else:
            more[i + 1] = more[i]
    
    count = 0
    for r in range(1, n + 1):
        # Find the smallest l such that the median of a[l:r+1] is m
        l = 0
        while l < r and (less[r] - less[l] <= (r - l) // 2) and (more[r] - more[l] <= (r - l) // 2):
            l += 1
        if l <= r:
            count += r - l + 1
    
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:]))
    
    result = count_median_pairs(n, m, a)
    print(result)

if __name__ == "__main__":
    main()