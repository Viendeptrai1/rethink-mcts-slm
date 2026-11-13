def find_squares(n):
    for m in range(int(n**0.5), -1, -1):
        m_squared = m * m
        k_squared = m_squared - n
        if k_squared >= 0:
            k = int(k_squared**0.5)
            if k * k == k_squared:
                return m, k
    return "impossible"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    n = int(input().strip())
    result = find_squares(n)
    if result == "impossible":
        print(result)
    else:
        print(result[0], result[1])