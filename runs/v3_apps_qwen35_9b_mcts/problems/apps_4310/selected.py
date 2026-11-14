import sys
import itertools

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    A = list(map(int, data))
    min_cost = float('inf')
    for p in itertools.permutations(A):
        cost = 0
        # First task cost is 0
        # Then cost to go from first to second
        cost += abs(p[1] - p[0])
        # Then cost to go from second to third
        cost += abs(p[2] - p[1])
        if cost < min_cost:
            min_cost = cost
    print(min_cost)

if __name__ == "__main__":
    solve()