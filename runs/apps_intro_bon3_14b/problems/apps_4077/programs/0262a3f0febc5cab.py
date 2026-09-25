import sys
from collections import Counter

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
        # Number of elements less than m in the subarray
        num_less = less[r]
        # Number of elements greater than m in the subarray
        num_more = more[r]
        
        # Length of the subarray
        length = r
        
        # Calculate the number of valid subarrays ending at r
        if length % 2 == 1:
            # Odd length, median is the middle element
            if num_less == num_more:
                count += 1
        else:
            # Even length, median is the left of the two middle elements
            if num_less == num_more + 1:
                count += 1
    
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