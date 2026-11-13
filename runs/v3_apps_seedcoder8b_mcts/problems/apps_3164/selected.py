def longest_consecutive_subarray():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    array = list(map(int, data[1:]))
    
    from collections import defaultdict
    
    left = 0
    max_length = 0
    count = defaultdict(int)
    unique_count = 0
    
    for right in range(N):
        count[array[right]] += 1
        
        if count[array[right]] == 1:
            unique_count += 1
        elif count[array[right]] == 2:
            unique_count += 1
        elif count[array[right]] == 3:
            unique_count -= 1
        
        while unique_count < right - left + 1:
            count[array[left]] -= 1
            if count[array[left]] == 1:
                unique_count += 1
            elif count[array[left]] == 0:
                unique_count -= 1
            left += 1
        
        if unique_count == right - left + 1:
            max_length = max(max_length, right - left + 1)
    
    print(max_length)