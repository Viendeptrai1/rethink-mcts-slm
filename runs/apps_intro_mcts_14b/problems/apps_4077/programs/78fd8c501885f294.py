import sys
from collections import defaultdict

def count_median_pairs(n, m, a):
    # Initialize prefix sums for counts of elements < m, = m, > m
    less_than_m = [0] * (n + 1)
    equal_to_m = [0] * (n + 1)
    greater_than_m = [0] * (n + 1)
    
    # Calculate prefix sums
    for i in range(1, n + 1):
        if a[i - 1] < m:
            less_than_m[i] = less_than_m[i - 1] + 1
            equal_to_m[i] = equal_to_m[i - 1]
            greater_than_m[i] = greater_than_m[i - 1]
        elif a[i - 1] == m:
            less_than_m[i] = less_than_m[i - 1]
            equal_to_m[i] = equal_to_m[i - 1] + 1
            greater_than_m[i] = greater_than_m[i - 1]
        else:
            less_than_m[i] = less_than_m[i - 1]
            equal_to_m[i] = equal_to_m[i - 1]
            greater_than_m[i] = greater_than_m[i - 1] + 1
    
    count = 0
    for l in range(1, n + 1):
        for r in range(l, n + 1):
            length = r - l + 1
            if length % 2 == 1:
                # Odd length, median is the middle element
                if equal_to_m[r] - equal_to_m[l - 1] >= 1:
                    count += 1
            else:
                # Even length, median is the left of the two middle elements
                if equal_to_m[r] - equal_to_m[l - 1] >= 1 and (less_than_m[r] - less_than_m[l - 1]) <= (equal_to_m[r] - equal_to_m[l - 1]):
                    count += 1
    
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