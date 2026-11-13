import sys
from collections import Counter

def solve():
    n, q = map(int, input().split())
    coins = Counter(map(int, input().split()))
    
    def min_coins(target):
        if target == 0:
            return 0
        
        total = 0
        for power in range(30, -1, -1):
            value = 1 << power
            if value > target:
                continue
            
            count = min(target // value, coins[value])
            target -= count * value
            total += count
        
        return total if target == 0 else -1
    
    for _ in range(q):
        b = int(input())
        print(min_coins(b))

if __name__ == "__main__":
    solve()