def find_unique_elements(grid):
    unique_rows = []
    unique_cols = []
    unique_blocks = []

    for i in range(9):
        row = set()
        col = set()
        block = set()
        for j in range(9):
            if grid[i][j] != '0':
                row.add(grid[i][j])
            if grid[j][i] != '0':
                col.add(grid[j][i])
            block_index = (i // 3) * 3 + j // 3
            if grid[block_index // 3 * 3 + j % 3][block_index % 3 * 3 + j // 3] != '0':
                block.add(grid[block_index // 3 * 3 + j % 3][block_index % 3 * 3 + j // 3])
        unique_rows.append(row)
        unique_cols.append(col)
        unique_blocks.append(block)

    return unique_rows, unique_cols, unique_blocks

def replace_unique_with_random(grid, unique_rows, unique_cols, unique_blocks):
    import random
    changes = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '0':
                continue
            row_set = unique_rows[i]
            col_set = unique_cols[j]
            block_index = (i // 3) * 3 + j // 3
            block_set = unique_blocks[block_index]
            possible_values = {str(x) for x in range(1, 10)} - (row_set | col_set | block_set)
            if possible_values:
                new_value = random.choice(list(possible_values))
                grid[i] = grid[i][:j] + new_value + grid[i][j+1:]
                changes += 1
                if changes >= 9:
                    return grid
    return grid

def solve(input_data):
    t = int(input_data.readline().strip())
    results = []
    for _ in range(t):
        grid = [input_data.readline().strip() for _ in range(9)]
        unique_rows, unique_cols, unique_blocks = find_unique_elements(grid)
        result_grid = replace_unique_with_random(grid, unique_rows, unique_cols, unique_blocks)
        results.append(result_grid)
    return '\n'.join('\n'.join(row) for row in results)

# Example usage:
# input_data = sys.stdin.read()
# output = solve(input_data)
# print(output)