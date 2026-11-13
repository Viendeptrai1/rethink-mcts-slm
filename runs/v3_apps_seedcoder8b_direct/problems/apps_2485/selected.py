def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    targets = data[3:]
    targets = [(int(targets[i]), int(targets[i+1])) for i in range(0, 2*M, 2)]
    
    from collections import defaultdict
    
    row_count = defaultdict(int)
    col_count = defaultdict(int)
    
    for h, w in targets:
        row_count[h] += 1
        col_count[w] += 1
    
    max_row = max(row_count.values(), default=0)
    max_col = max(col_count.values(), default=0)
    
    # Find the number of rows and columns that have the maximum number of targets
    max_row_count = sum(1 for count in row_count.values() if count == max_row)
    max_col_count = sum(1 for count in col_count.values() if count == max_col)
    
    # Calculate the maximum number of targets destroyable
    max_targets = max_row * max_col_count + max_col * max_row_count - max_row * max_col
    
    print(max_targets)

if __name__ == "__main__":
    main()