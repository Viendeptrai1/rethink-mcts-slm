import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    # Count occurrences of elements less than, equal to, and greater than m
    less_count = [0] * (n + 1)
    equal_count = [0] * (n + 1)
    greater_count = [0] * (n + 1)
    
    for i in range(n):
        if a[i] < m:
            less_count[i + 1] = less_count[i] + 1
            equal_count[i + 1] = equal_count[i]
            greater_count[i + 1] = greater_count[i]
        elif a[i] == m:
            less_count[i + 1] = less_count[i]
            equal_count[i + 1] = equal_count[i] + 1
            greater_count[i + 1] = greater_count[i]
        else:
            less_count[i + 1] = less_count[i]
            equal_count[i + 1] = equal_count[i]
            greater_count[i + 1] = greater_count[i] + 1
    
    # Calculate the number of valid subarrays
    result = 0
    for l in range(n + 1):
        for r in range(l + 1, n + 1):
            if equal_count[r] - equal_count[l] > 0:
                if less_count[r] - less_count[l] <= equal_count[r] - equal_count[l]:
                    if greater_count[r] - greater_count[l] >= equal_count[r] - equal_count[l]:
                        result += 1
    
    print(result)

if __name__ == "__main__":
    main()