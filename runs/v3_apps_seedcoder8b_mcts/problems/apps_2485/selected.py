def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    targets = data[3:]
    
    from collections import defaultdict
    
    row_count = defaultdict(int)
    col_count = defaultdict(int)
    
    for i in range(M):
        h = int(targets[2 * i])
        w = int(targets[2 * i + 1])
        row_count[h] += 1
        col_count[w] += 1
    
    max_row = max(row_count.values(), default=0)
    max_col = max(col_count.values(), default=0)
    
    # Find the number of rows and columns that have the maximum number of targets
    max_row_count = sum(1 for count in row_count.values() if count == max_row)
    max_col_count = sum(1 for count in col_count.values() if count == max_col)
    
    # Calculate the maximum number of targets destroyable
    max_targets = max_row + max_col
    
    # If there are multiple rows and columns with the same maximum, we can overlap
    if max_row_count > 1 and max_col_count > 1:
        # Overlap area is (max_row_count - 1) * (max_col_count - 1)
        overlap_area = (max_row_count - 1) * (max_col_count - 1)
        max_targets = max(max_targets, max_row + max_col - overlap_area)
    
    print(max_targets)

if __name__ == "__main__":
    main()