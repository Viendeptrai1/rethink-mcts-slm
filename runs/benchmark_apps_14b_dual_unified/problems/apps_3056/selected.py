def calculate_walk_value(pattern):
    def dfs(index, current_value):
        if index == len(pattern):
            return current_value
        
        char = pattern[index]
        if char == 'L':
            return dfs(index + 1, current_value * 2)
        elif char == 'R':
            return dfs(index + 1, current_value * 2 + 1)
        elif char == 'P':
            return dfs(index + 1, current_value)
        else:  # char == '*'
            return (dfs(index + 1, current_value * 2) +
                    dfs(index + 1, current_value * 2 + 1) +
                    dfs(index + 1, current_value))
    
    return dfs(0, 1)

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Calculate and print the result
print(calculate_walk_value(input))