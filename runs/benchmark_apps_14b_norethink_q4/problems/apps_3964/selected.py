def count_good_plans(n, m, b, mod, a):
    def backtrack(index, remaining_lines, current_bugs):
        if remaining_lines == 0:
            return 1 if current_bugs <= b else 0
        if index == n or current_bugs > b:
            return 0
        
        count = 0
        max_lines = min(remaining_lines, (b - current_bugs) // a[index])
        
        for lines in range(max_lines + 1):
            count += backtrack(index + 1, remaining_lines - lines, current_bugs + lines * a[index])
            count %= mod
        
        return count
    
    return backtrack(0, m, 0)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
b = int(data[2])
mod = int(data[3])
a = list(map(int, data[4:]))

# Output the result
print(count_good_plans(n, m, b, mod, a))