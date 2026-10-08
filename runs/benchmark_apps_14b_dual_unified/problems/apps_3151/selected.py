import sys

def find_pool_and_building_dimensions(n):
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            a = n // i
            b = i
            if (a + b) % 2 == 0 and (a - b) % 2 == 0:
                m = (a + b) // 2
                k = (a - b) // 2
                return m, k
    return "impossible"

def main():
    import sys
    n = int(sys.stdin.read().strip())
    result = find_pool_and_building_dimensions(n)
    if result == "impossible":
        print("impossible")
    else:
        m, k = result
        print(m, k)

if __name__ == "__main__":
    main()