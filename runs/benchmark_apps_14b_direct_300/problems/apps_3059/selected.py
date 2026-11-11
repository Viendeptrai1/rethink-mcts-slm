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
        if index == m:
            return max(current_time, n)
        
        t, p, d = tricks[index]
        if current_time + t >= r:
            return max(current_time + t, n)
        
        # Option 1: Attempt the trick
        attempt_time = current_time + t
        if attempt_time >= r:
            return max(attempt_time, n)
        
        success_time = expected_time(index + 1, attempt_time)
        failure_time = expected_time(index, current_time + d)
        
        expected = p * success_time + (1 - p) * failure_time
        
        # Option 2: Reset and start over
        reset_time = expected_time(0, 0)
        
        return min(expected, reset_time)
    
    result = expected_time(0, 0)
    print(f"{result:.6f}")

if __name__ == "__main__":
    main()