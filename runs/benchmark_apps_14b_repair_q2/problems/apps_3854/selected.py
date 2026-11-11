import sys
from itertools import combinations

def solve():
    import sys
    from itertools import combinations

    def solve():
        n, k = map(int, sys.stdin.readline().split())
        coins = list(map(int, sys.stdin.readline().split()))

        # Find all subsets that sum up to k
        valid_subsets = []
        for r in range(1, n + 1):
            for subset in combinations(coins, r):
                if sum(subset) == k:
                    valid_subsets.append(subset)

        # Find all possible sums that can be made from these subsets
        possible_sums = set()
        for subset in valid_subsets:
            for r in range(len(subset) + 1):
                for subsubset in combinations(subset, r):
                    possible_sums.add(sum(subsubset))

        # Convert the set to a sorted list
        possible_sums = sorted(list(possible_sums))

        # Output the result
        print(len(possible_sums))
        print(" ".join(map(str, possible_sums)))

    solve()

solve()