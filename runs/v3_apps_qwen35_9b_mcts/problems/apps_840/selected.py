import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
            
        b = []
        for _ in range(n):
            b.append(int(next(iterator)))
    except StopIteration:
        return

    def can_make(x):
        needed = 0
        for i in range(n):
            required = a[i] * x
            if b[i] >= required:
                continue
            else:
                needed += (required - b[i])
        
        return needed <= k

    low = 0
    high = 2 * 10**18  # Sufficiently large upper bound
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        if can_make(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()