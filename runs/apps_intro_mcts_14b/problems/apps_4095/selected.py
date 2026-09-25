import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = list(map(int, data[2:]))
    
    # Initialize prefix sums
    prefix_less = [0] * (n + 1)
    prefix_equal = [0] * (n + 1)
    prefix_greater = [0] * (n + 1)
    
    # Calculate prefix sums
    for i in range(n):
        if p[i] < m:
            prefix_less[i + 1] = prefix_less[i] + 1
            prefix_equal[i + 1] = prefix_equal[i]
            prefix_greater[i + 1] = prefix_greater[i]
        elif p[i] == m:
            prefix_less[i + 1] = prefix_less[i]
            prefix_equal[i + 1] = prefix_equal[i] + 1
            prefix_greater[i + 1] = prefix_greater[i]
        else:
            prefix_less[i + 1] = prefix_less[i]
            prefix_equal[i + 1] = prefix_equal[i]
            prefix_greater[i + 1] = prefix_greater[i] + 1
    
    count = 0
    
    # Iterate over all possible subarrays
    for r in range(1, n + 1):
        # We need the number of elements less than m to be equal to or one less than the number of elements greater than m
        # And the number of elements equal to m should be at least 1
        less_count = prefix_less[r]
        equal_count = prefix_equal[r]
        greater_count = prefix_greater[r]
        
        # Check for valid subarrays ending at r
        for l in range(r):
            if equal_count - prefix_equal[l] >= 1:
                if less_count - prefix_less[l] == greater_count - prefix_greater[l]:
                    count += 1
                elif less_count - prefix_less[l] + 1 == greater_count - prefix_greater[l]:
                    count += 1
    
    print(count)

if __name__ == "__main__":
    main()