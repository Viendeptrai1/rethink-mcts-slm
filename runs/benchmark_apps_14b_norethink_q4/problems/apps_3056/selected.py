import sys

def calculate_walk_value(pattern):
    def dfs(index, current_value):
        if index == len(pattern):
            return current_value
        if pattern[index] == '*':
            return (dfs(index + 1, current_value * 2) +
                    dfs(index + 1, current_value * 2 + 1) +
                    dfs(index + 1, current_value))
        elif pattern[index] == 'L':
            return dfs(index + 1, current_value * 2)
        elif pattern[index] == 'R':
            return dfs(index + 1, current_value * 2 + 1)
        elif pattern[index] == 'P':
            return dfs(index + 1, current_value)

    return dfs(0, 1)

if __name__ == "__main__":
    pattern = input().strip()
    result = calculate_walk_value(pattern)
    print(result)