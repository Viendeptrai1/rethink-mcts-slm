def max_rectangle_area():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    if N < 4:
        print(0)
        return
    
    A.sort()
    
    # The largest four sticks
    largest_four = A[-4:]
    
    # Check all combinations of two pairs from the largest four
    max_area = 0
    for i in range(4):
        for j in range(i + 1, 4):
            # The two pairs are (largest_four[i], largest_four[j]) and (largest_four[k], largest_four[l])
            for k in range(j + 1, 4):
                for l in range(k + 1, 4):
                    area = min(largest_four[i], largest_four[j]) * min(largest_four[k], largest_four[l])
                    max_area = max(max_area, area)
    
    print(max_area)