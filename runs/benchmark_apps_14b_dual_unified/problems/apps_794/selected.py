import sys
from itertools import combinations

def can_reorder(a, n):
    total_sum = sum(a)
    
    # If the total sum is odd, it's always possible to split into two unequal parts
    if total_sum % 2 != 0:
        return True
    
    # If the total sum is even, check if there exists a subset with a sum different from half of the total sum
    half_sum = total_sum // 2
    for r in range(1, n + 1):
        for subset in combinations(a, r):
            if sum(subset) != half_sum:
                return True
    
    return False

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    if not can_reorder(a, n):
        print("-1")
        return
    
    # Try to find a valid reordering
    for perm in permutations(a):
        if sum(perm[:n]) != sum(perm[n:]):
            print(" ".join(map(str, perm)))
            return
    
    # If no valid reordering is found, which theoretically shouldn't happen due to the earlier check
    print("-1")

if __name__ == "__main__":
    main()