import sys

def find_swimming_pool_dimensions(n):
    for m in range(1, int((n + 1) ** 0.5) + 1):
        k_squared = m * m - n
        if k_squared >= 0:
            k = int(k_squared ** 0.5)
            if k * k == k_squared:
                return m, k
    return "impossible"

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = find_swimming_pool_dimensions(n)
    if result == "impossible":
        print("impossible")
    else:
        m, k = result
        print(m, k)