def check_records():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    T = int(data[index])
    index += 1
    
    results = []
    
    for _ in range(T):
        n = int(data[index])
        index += 1
        
        prev_p = 0
        prev_c = 0
        
        valid = True
        for _ in range(n):
            p = int(data[index])
            c = int(data[index + 1])
            index += 2
            
            if p < prev_p or c > prev_c or (c == prev_c and p != prev_p):
                valid = False
                break
            
            prev_p = p
            prev_c = c
        
        results.append("YES" if valid else "NO")
    
    for result in results:
        print(result)

check_records()