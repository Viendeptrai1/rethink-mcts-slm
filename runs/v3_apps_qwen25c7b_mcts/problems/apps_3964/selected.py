from functools import lru_cache

def count_good_plans(n, m, b, mod, a):
    @lru_cache(None)
    def dp(i, lines_left, max_bugs):
        if lines_left == 0:
            return 1 if max_bugs >= 0 else 0
        if i == n or max_bugs < 0:
            return 0
        result = 0
        for k in range(lines_left + 1):
            result += dp(i + 1, lines_left - k, max_bugs - k * a[i])
            result %= mod
        return result

    return dp(0, m, b)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    b = int(data[2])
    mod = int(data[3])
    a = list(map(int, data[4:]))

    print(count_good_plans(n, m, b, mod, a))