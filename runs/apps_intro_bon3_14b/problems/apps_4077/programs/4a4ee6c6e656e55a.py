import sys
from collections import defaultdict

def count_median_pairs(n, m, a):
    # Create a prefix sum array for elements less than m
    less = [0] * (n + 1)
    # Create a prefix sum array for elements equal to m
    equal = [0] * (n + 1)
    
    for i in range(n):
        less[i + 1] = less[i] + (1 if a[i] < m else 0)
        equal[i + 1] = equal[i] + (1 if a[i] == m else 0)
    
    count = 0
    for r in range(1, n + 1):
        # Calculate the number of valid subarrays ending at r
        # We need the number of elements less than m to be equal to or one more than the number of elements equal to m
        # This can be achieved by finding the number of l such that:
        # less[r] - less[l] <= equal[r] - equal[l]
        # Rearranging gives:
        # less[r] - equal[r] <= less[l] - equal[l]
        target = less[r] - equal[r]
        count += equal[r] + (less[r] - equal[r] >= 0)
    
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