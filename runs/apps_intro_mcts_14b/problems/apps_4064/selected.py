import sys
from functools import lru_cache

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    h = int(data[1])
    l = int(data[2])
    r = int(data[3])
    
    a = list(map(int, data[4:]))
    
    @lru_cache(None)
    def dp(i, t):
        if i == n:
            return 0
        # Option 1: Sleep after a[i] hours
        t1 = (t + a[i]) % h
        good_count1 = dp(i + 1, t1) + (1 if l <= t1 <= r else 0)
        
        # Option 2: Sleep after a[i] - 1 hours
        t2 = (t + a[i] - 1) % h
        good_count2 = dp(i + 1, t2) + (1 if l <= t2 <= r else 0)
        
        return max(good_count1, good_count2)
    
    result = dp(0, 0)
    print(result)

if __name__ == "__main__":
    main()