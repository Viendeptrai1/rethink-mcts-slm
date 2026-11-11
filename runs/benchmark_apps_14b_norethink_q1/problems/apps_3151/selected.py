import sys

def find_m_k(n):
    if n % 4 == 0 or n % 2 == 1:
        m = (n + 1) // 2
        k = (n - 1) // 2
        return m, k
    else:
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