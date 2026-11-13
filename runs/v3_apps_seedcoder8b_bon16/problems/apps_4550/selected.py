def can_distribute_equally(a, b, c):
    total_candies = a + b + c
    if total_candies % 2 != 0:
        return "No"
    target = total_candies // 2
    return "Yes" if target in [a, b, c] else "No"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    a, b, c = map(int, data.split())
    print(can_distribute_equally(a, b, c))