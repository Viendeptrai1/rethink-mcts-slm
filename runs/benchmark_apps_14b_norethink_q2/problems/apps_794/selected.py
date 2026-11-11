import sys
from itertools import combinations

def can_reorder(a, n):
    total_sum = sum(a)
    if total_sum % 2 != 0:
        return -1
    
    target_sum = total_sum // 2
    
    # Check all combinations of the first n elements
    for comb in combinations(a, n):
        if sum(comb) == target_sum:
            return -1
    
    # If no valid combination is found, return the original array
    return a

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = can_reorder(a, n)
    
    if result == -1:
        print("-1")
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()