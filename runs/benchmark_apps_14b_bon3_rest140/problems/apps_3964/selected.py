import sys
from functools import lru_cache

def count_good_plans(n, m, b, mod, a):
    @lru_cache(None)
    def dp(i, remaining_lines, total_bugs):
        if i == n:
            return 1 if remaining_lines == 0 and total_bugs <= b else 0
        if remaining_lines < 0 or total_bugs > b:
            return 0
        
        count = 0
        for lines_written_by_i in range(remaining_lines + 1):
            count += dp(i + 1, remaining_lines - lines_written_by_i, total_bugs + lines_written_by_i * a[i])
            count %= mod
        
        return count
    
    return dp(0, m, 0)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    b = int(data[2])
    mod = int(data[3])
    a = list(map(int, data[4:]))
    
    result = count_good_plans(n, m, b, mod, a)
    print(result)

if __name__ == "__main__":
    main()