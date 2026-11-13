def max_targets_destruction():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    target_positions = set()
    
    index = 3
    for _ in range(M):
        h_i = int(data[index])
        w_i = int(data[index + 1])
        target_positions.add((h_i, w_i))
        index += 2
    
    row_count = {}
    col_count = {}
    
    for h, w in target_positions:
        if h in row_count:
            row_count[h] += 1
        else:
            row_count[h] = 1
            
        if w in col_count:
            col_count[w] += 1
        else:
            col_count[w] = 1
    
    max_row_destroys = max(row_count.values(), default=0)
    max_col_destroys = max(col_count.values(), default=0)
    
    max_destroys = max_row_destroys + max_col_destroys
    
    if max_destroys > M:
        max_destroys = M
    
    print(max_destroys)

max_targets_destruction()