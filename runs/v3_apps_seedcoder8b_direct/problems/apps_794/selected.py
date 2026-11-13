def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    total_sum = sum(a)
    
    if total_sum % 2 == 0:
        print(-1)
        return
    
    half_sum = total_sum // 2
    
    a.sort()
    
    first_half = []
    second_half = []
    
    current_sum = 0
    
    for num in a:
        if current_sum < half_sum:
            first_half.append(num)
            current_sum += num
        else:
            second_half.append(num)
    
    if current_sum != half_sum:
        print(-1)
        return
    
    result = first_half + second_half
    print(" ".join(map(str, result)))