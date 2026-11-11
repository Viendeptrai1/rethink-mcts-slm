import sys
from functools import lru_cache

def main():
    import sys
    import math
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    def readfloats():
        return list(map(float, sys.stdin.readline().split()))
    
    n, r, m = readints()
    tricks = [readfloats() for _ in range(m)]
    
    @lru_cache(None)
    def expected_time(index, current_time):
        if current_time >= r:
            return 0
        if index == m:
            return n - current_time
        
        t, p, d = tricks[index]
        if current_time + t >= r:
            return 0
        
        # Option 1: Attempt the trick
        attempt_time = t + expected_time(index + 1, current_time + t)
        # Option 2: Reset and try again
        reset_time = (1 / p) * (t + d + expected_time(index, 0))
        
        return min(attempt_time, reset_time)
    
    result = expected_time(0, 0)
    print(f"{result:.6f}")

if __name__ == "__main__":
    main()