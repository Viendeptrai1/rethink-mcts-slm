def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        
        if n % 2 != 0:
            results.append("NO")
            continue
        
        half_n = n // 2
        even_sum = half_n * (half_n + 1)
        odd_sum = even_sum
        
        if even_sum == odd_sum:
            results.append("YES")
            even_part = [2 * i for i in range(1, half_n + 1)]
            odd_part = [2 * i - 1 for i in range(1, half_n + 1)]
            results.append(" ".join(map(str, even_part + odd_part)))
        else:
            results.append("NO")
    
    for result in results:
        print(result)