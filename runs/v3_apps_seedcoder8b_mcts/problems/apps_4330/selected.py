def find_k(a, b):
    if a == b:
        return "IMPOSSIBLE"
    k = (a + b) // 2
    if abs(a - k) == abs(b - k):
        return k
    else:
        return "IMPOSSIBLE"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    a, b = map(int, data.split())
    result = find_k(a, b)
    print(result)