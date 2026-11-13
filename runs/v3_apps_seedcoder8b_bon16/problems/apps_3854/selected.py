def solve():
    n, k = map(int, input().split())
    coins = list(map(int, input().split()))
    
    def can_make(target, start, end):
        if target == 0:
            return True
        if start > end or target < 0:
            return False
        return can_make(target - coins[start], start + 1, end) or can_make(target, start + 1, end)
    
    reachable = set()
    for i in range(n):
        for j in range(i, n):
            subset_sum = sum(coins[i:j+1])
            if subset_sum <= k and can_make(k - subset_sum, 0, n - 1):
                reachable.add(subset_sum)
    
    reachable.add(0)
    reachable.add(k)
    
    print(len(reachable))
    print(*sorted(reachable))

if __name__ == "__main__":
    solve()