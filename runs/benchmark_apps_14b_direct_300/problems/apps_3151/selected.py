import sys

def find_m_k(n):
    for m in range(1, int((n + 1) ** 0.5) + 1):
        k_squared = m * m - n
        if k_squared >= 0:
            k = int(k_squared ** 0.5)
            if k * k == k_squared:
                return m, k
    return None

def main():
    import sys
    n = int(sys.stdin.read().strip())
    result = find_m_k(n)
    if result:
        m, k = result
        print(m, k)
    else:
        print("impossible")

if __name__ == "__main__":
    main()