import sys
from typing import List

def count_unnecessary_cards(N: int, K: int, a: List[int]) -> int:
    # Helper function to check if a subset is good
    def is_good_subset(subset_sum: int) -> bool:
        return subset_sum >= K
    
    # Bitmask to generate all subsets
    total_subsets = 1 << N
    necessary_count = 0
    
    for mask in range(total_subsets):
        subset_sum = 0
        for j in range(N):
            if mask & (1 << j):
                subset_sum += a[j]
        
        if is_good_subset(subset_sum):
            # Check if removing any card makes the subset bad
            remove_possible = False
            for j in range(N):
                if mask & (1 << j):
                    new_mask = mask ^ (1 << j)
                    new_subset_sum = subset_sum - a[j]
                    if is_good_subset(new_subset_sum):
                        remove_possible = True
                        break
            if not remove_possible:
                necessary_count += 1
                
    return necessary_count

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(count_unnecessary_cards(N, K, a))