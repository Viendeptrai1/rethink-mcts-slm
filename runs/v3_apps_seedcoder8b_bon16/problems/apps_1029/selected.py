def max_original_array_length(p):
    p = int(p)
    length = 1
    
    while p > 9:
        p_str = str(p)
        max_split = 0
        
        for i in range(1, len(p_str)):
            left = int(p_str[:i])
            right = int(p_str[i:])
            if right > 0 and left % right == 0:
                max_split = max(max_split, left // right)
        
        if max_split == 0:
            break
        
        p = max_split
        length += 1
    
    return length

# Read input and print result
p = input().strip()
print(max_original_array_length(p))