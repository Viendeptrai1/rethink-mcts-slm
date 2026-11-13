def check_takahashi_statement():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    # Convert input strings to integers
    c = [[int(data[3*i + j]) for j in range(3)] for i in range(3)]
    
    # Check rows for consistency
    row_diffs = [set(c[i][j+1] - c[i][j] for j in range(2)) for i in range(3)]
    if len(set(map(len, row_diffs))) != 1:
        return "No"
    
    # Check columns for consistency
    col_diffs = [set(c[j+1][i] - c[j][i] for j in range(2)) for i in range(3)]
    if len(set(map(len, col_diffs))) != 1:
        return "No"
    
    return "Yes"

# Call the function and print the result
print(check_takahashi_statement())