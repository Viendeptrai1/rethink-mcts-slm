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
        hi = r
        while l < hi:
            mid = (l + hi) // 2
            if (r - mid + 1) % 2 == 1:
                # Odd length subarray
                if less[r] - less[mid] <= (r - mid + 1) // 2 and more[r] - more[mid] <= (r - mid + 1) // 2:
                    hi = mid
                else:
                    l = mid + 1
            else:
                # Even length subarray
                if less[r] - less[mid] <= (r - mid) // 2 and more[r] - more[mid] <= (r - mid) // 2:
                    hi = mid
                else:
                    l = mid + 1
        
        count += r - l + 1
    
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    result = count_median_pairs(n, m, a)
    print(result)

if __name__ == "__main__":
    main()