import sys
import functools

def expected_max(m, n):
    @functools.lru_cache(None)
    def dp(max_so_far, rolls_left):
        if rolls_left == 0:
            return max_so_far
        total = 0
        for i in range(1, m + 1):
            total += dp(max(max_so_far, i), rolls_left - 1)
        return total / m

    return dp(0, n)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    m = int(data[0])
    n = int(data[1])
    result = expected_max(m, n)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()