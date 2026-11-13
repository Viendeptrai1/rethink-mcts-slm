import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    A = list(map(int, data))
    A.sort()
    # Optimal strategy: start at min, go to max, then to the remaining middle value
    # Cost = (max - min) + (max - middle) = 2*max - min - middle
    # Alternatively, since there are only 3 tasks, we can just compute the two possible paths:
    # Path 1: min -> middle -> max: cost = (middle - min) + (max - middle) = max - min
    # Path 2: min -> max -> middle: cost = (max - min) + (max - middle) = 2*max - min - middle
    # Path 3: middle -> min -> max: cost = (middle - min) + (max - min) = 2*min - 2*middle + max? No.
    # Actually, let's enumerate all permutations of the 3 tasks.
    # First task cost 0.
    # Then cost = |A[j] - A[i]| + |A[k] - A[j]|
    # We try all 6 permutations.
    
    import itertools
    perms = itertools.permutations(A)
    min_cost = float('inf')
    for p in perms:
        # p[0] is first (cost 0)
        # p[1] is second (cost |p[1] - p[0]|)
        # p[2] is third (cost |p[2] - p[1]|)
        cost = abs(p[1] - p[0]) + abs(p[2] - p[1])
        if cost < min_cost:
            min_cost = cost
    print(min_cost)

if __name__ == "__main__":
    solve()