import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    n = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    
    a = []
    for _ in range(n):
        a.append(int(data[idx]))
        idx += 1
    
    b = []
    for _ in range(n):
        b.append(int(data[idx]))
        idx += 1
    
    def can_bake(x):
        needed = 0
        for i in range(n):
            cost = a[i] * x
            have = b[i]
            if cost > have:
                needed += (cost - have)
            if needed > k:
                return False
        return True

    low = 0
    high = 2000000000 * n  # Safe upper bound
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        if can_bake(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    
    print(ans)

if __name__ == "__main__":
    solve()