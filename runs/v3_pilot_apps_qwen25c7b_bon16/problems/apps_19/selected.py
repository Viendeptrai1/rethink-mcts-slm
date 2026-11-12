def check_records():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    def get_int():
        nonlocal index
        result = int(data[index])
        index += 1
        return result
    
    def get_pair():
        nonlocal index
        p = get_int()
        c = get_int()
        index += 1
        return p, c
    
    t = get_int()
    results = []
    for _ in range(t):
        n = get_int()
        prev_p, prev_c = 0, 0
        valid = True
        for _ in range(n):
            p, c = get_pair()
            if p < prev_p or c > prev_c or (c == prev_c and p != prev_p):
                valid = False
                break
            prev_p, prev_c = p, c
        results.append("YES" if valid else "NO")
    
    print("\n".join(results))

check_records()