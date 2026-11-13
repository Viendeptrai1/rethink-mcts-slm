def count_ways_to_fill_grid(n, k):
    MOD = 10**9 + 7
    
    # Calculate the number of ways to fill the grid
    # For each row, we have k choices for the first cell, k-1 for the second, and so on.
    # For each column, we have k choices for the first cell, k-1 for the second, and so on.
    # However, we need to ensure that each row and column has at least one '1'.
    
    # Total ways to fill the grid without constraints
    total_ways = pow(k, n * n, MOD)
    
    # Subtract the invalid configurations where a row or column has no '1'
    
    # Ways to fill n rows with at least one '1'
    ways_to_fill_rows = pow(k - 1, n, MOD) * n
    
    # Ways to fill n columns with at least one '1'
    ways_to_fill_columns = pow(k - 1, n, MOD) * n
    
    # Subtract the double-counted invalid configurations where both a row and a column have no '1'
    invalid_configurations = pow(k - 1, n, MOD) * n * n
    
    # Calculate the final result
    result = (total_ways - ways_to_fill_rows - ways_to_fill_columns + invalid_configurations) % MOD
    
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k = map(int, data.split())
    print(count_ways_to_fill_grid(n, k))