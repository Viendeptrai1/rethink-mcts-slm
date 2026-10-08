def max_elements(p):
    p_str = str(p)
    n = len(p_str)
    
    def dfs(start, count):
        if start == n:
            return count
        max_count = count
        for end in range(start + 1, n + 1):
            num = int(p_str[start:end])
            if num > 0:
                max_count = max(max_count, dfs(end, count + 1))
        return max_count
    
    return dfs(0, 0)

# Read input from stdin
import sys
input = sys.stdin.read().strip()
p = int(input)

# Print the result
print(max_elements(p))