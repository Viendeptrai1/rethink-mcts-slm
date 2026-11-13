def solve():
    n = int(input())
    heights = list(map(int, input().split()))
    
    count = [0] * (2 * 10**5 + 1)
    for height in heights:
        count[height] += 1
    
    max_length = 0
    start_height = 0
    
    for height in range(1, 2 * 10**5 + 1):
        current_length = 0
        for h in range(height, min(height + 2, 2 * 10**5 + 1)):
            current_length += count[h]
        
        if current_length > max_length:
            max_length = current_length
            start_height = height
    
    result = []
    for h in range(start_height, min(start_height + 2, 2 * 10**5 + 1)):
        result.extend([h] * count[h])
    
    print(max_length)
    print(*result[:max_length])

solve()