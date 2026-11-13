def check_box_sizes(V):
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    V = int(data[1])
    
    boxes = []
    index = 2
    for _ in range(n):
        l = int(data[index])
        w = int(data[index + 1])
        h = int(data[index + 2])
        volume = l * w * h
        boxes.append((volume, l, w, h))
        index += 3
    
    max_box = max(boxes)
    d_i = max_box[0] - V
    
    return d_i

# Call the function to read input and get the result
result = check_box_sizes(None)
print(result)