import sys
from itertools import combinations

def main():
    import sys
    import itertools

    def read_ints():
        return list(map(int, sys.stdin.readline().split()))

    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]

    max_diff = 0
    best_segments = []

    # Check all subsets of segments
    for r in range(1, m + 1):
        for subset in itertools.combinations(range(m), r):
            b = a[:]
            for idx in subset:
                l, r = segments[idx]
                for i in range(l - 1, r):
                    b[i] -= 1
            current_max = max(b)
            current_min = min(b)
            current_diff = current_max - current_min
            if current_diff > max_diff:
                max_diff = current_diff
                best_segments = subset

    print(max_diff)
    print(len(best_segments))
    print(' '.join(map(str, [x + 1 for x in best_segments])))

if __name__ == "__main__":
    main()