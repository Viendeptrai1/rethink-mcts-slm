import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    a = list(map(int, data))
    total_sum = sum(a)
    if total_sum % 2 != 0:
        print("NO")
        return
    target = total_sum // 2
    # Check all combinations of 3 students
    n = 6
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if a[i] + a[j] + a[k] == target:
                    print("YES")
                    return
    print("NO")

if __name__ == "__main__":
    solve()