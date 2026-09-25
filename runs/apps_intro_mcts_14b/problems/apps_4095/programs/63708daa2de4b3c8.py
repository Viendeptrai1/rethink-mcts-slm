import sys
from typing import List

def update(fenwick_tree: List[int], index: int, delta: int) -> None:
    while index < len(fenwick_tree):
        fenwick_tree[index] += delta
        index += index & -index

def query(fenwick_tree: List[int], index: int) -> int:
    result = 0
    while index > 0:
        result += fenwick_tree[index]
        index -= index & -index
    return result

def count_median_pairs(n: int, m: int, p: List[int]) -> int:
    # Create a Fenwick Tree to count occurrences of numbers less than and greater than m
    fenwick_tree_less = [0] * (n + 1)
    fenwick_tree_greater = [0] * (n + 1)
    
    # Count the number of elements less than and greater than m
    count_less = 0
    count_greater = 0
    for i in range(n):
        if p[i] < m:
            count_less += 1
        elif p[i] > m:
            count_greater += 1
        update(fenwick_tree_less, p[i], 1)
        update(fenwick_tree_greater, p[i], 1)
    
    # Calculate the number of valid subarrays
    result = 0
    for i in range(n):
        # If p[i] == m, we need to consider subarrays ending at i
        if p[i] == m:
            # Number of elements less than m in the current subarray
            less_count = query(fenwick_tree_less, m - 1)
            # Number of elements greater than m in the current subarray
            greater_count = query(fenwick_tree_greater, n) - query(fenwick_tree_greater, m)
            # The median is m if the number of elements less than or equal to m is at least (i + 1) // 2
            if less_count + (i + 1) // 2 <= (i + 1) // 2 + greater_count:
                result += 1
        
        # Update the Fenwick Trees for the next iteration
        if p[i] < m:
            count_less -= 1
        elif p[i] > m:
            count_greater -= 1
        update(fenwick_tree_less, p[i], -1)
        update(fenwick_tree_greater, p[i], -1)
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = list(map(int, data[2:]))
    
    result = count_median_pairs(n, m, p)
    print(result)

if __name__ == "__main__":
    main()