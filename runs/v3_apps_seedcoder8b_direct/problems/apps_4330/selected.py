def find_k(a, b):
    if (a + b) % 2 == 0:
        return (a + b) // 2
    else:
        return "IMPOSSIBLE"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    a, b = map(int, data.split())
    result = find_k(a, b)
    print(result)