def calculate_walk_value(walk_set: str) -> int:
    MOD = 10**9 + 7

    def dfs(index: int, current_value: int) -> int:
        if index == len(walk_set):
            return current_value
        
        if walk_set[index] == 'L':
            return dfs(index + 1, current_value * 2)
        elif walk_set[index] == 'R':
            return dfs(index + 1, current_value * 2 + 1)
        elif walk_set[index] == 'P':
            return dfs(index + 1, current_value)
        elif walk_set[index] == '*':
            total_value = 0
            total_value += dfs(index + 1, current_value * 2)  # 'L'
            total_value += dfs(index + 1, current_value * 2 + 1)  # 'R'
            total_value += dfs(index + 1, current_value)  # 'P'
            return total_value % MOD

    return dfs(0, 1)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(calculate_walk_value(input))