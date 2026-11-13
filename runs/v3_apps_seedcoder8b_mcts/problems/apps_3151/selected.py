import sys
import math

def find_squares(n):
    for m in range(int(math.sqrt(n)) + 1, 0, -1):
        m_squared = m * m
        if m_squared > n:
            continue
        k_squared = m_squared - n
        if k_squared < 0:
            break
        k = int(math.sqrt(k_squared))
        if k * k == k_squared:
            return m, k
    return "impossible"

def main():
    input_data = sys.stdin.read().strip()
    n = int(input_data)
    result = find_squares(n)
    if result == "impossible":
        print(result)
    else:
        print(f"{result[0]} {result[1]}")

if __name__ == "__main__":
    main()