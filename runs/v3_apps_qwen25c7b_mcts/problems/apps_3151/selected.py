import math

def find_dimensions(n):
    for k in range(1, int(math.sqrt(n / 2)) + 1):
        m_squared = n + k * k
        m = int(math.isqrt(m_squared))
        if m * m == m_squared:
            return m, k
    return "impossible"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n = int(data)
    result = find_dimensions(n)
    print(result)