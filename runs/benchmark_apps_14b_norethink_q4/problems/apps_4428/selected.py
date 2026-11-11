import sys
from typing import List

def max_sum_split(n: int, d: List[int]) -> int:
    # Calculate prefix sums from the left
    left_prefix_sums = [0] * (n + 1)
    for i in range(1, n + 1):
        left_prefix_sums[i] = left_prefix_sums[i - 1] + d[i - 1]
    
    # Calculate prefix sums from the right
    right_prefix_sums = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        right_prefix_sums[i] = right_prefix_sums[i + 1] + d[i]
    
    max_sum = 0
    
    # Iterate over all possible positions for the middle part
    for mid_start in range(n + 1):
        # Iterate over all possible lengths of the first part
        for first_part_length in range(mid_start + 1):
            sum1 = left_prefix_sums[first_part_length]
            sum3 = right_prefix_sums[mid_start]
            
            if sum1 == sum3:
                max_sum = max(max_sum, sum1)
    
    return max_sum

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = list(map(int, data[1:]))
    
    result = max_sum_split(n, d)
    print(result)