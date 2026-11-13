MOD = 10**9 + 7

def count_random_pictures(n, m):
    if n % 2 == 0:
        return pow(2, n * m, MOD)
    else:
        return (pow(2, n * m // 2, MOD) + pow(2, (n * m + 1) // 2, MOD)) % MOD

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    m = int(data[1])
    print(count_random_pictures(n, m))