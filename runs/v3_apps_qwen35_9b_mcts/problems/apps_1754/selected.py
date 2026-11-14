import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    k = int(next(iterator))
    
    p = []
    for _ in range(n):
        p.append(int(next(iterator)))
        
    s = []
    for _ in range(n):
        s.append(int(next(iterator)))
        
    c = []
    for _ in range(k):
        c.append(int(next(iterator)))
        
    # Map school_id -> max_power
    school_max = {}
    for i in range(n):
        school_id = s[i]
        power = p[i]
        if school_id not in school_max:
            school_max[school_id] = power
        else:
            school_max[school_id] = max(school_max[school_id], power)
            
    needed = 0
    for chosen_id in c:
        chosen_id -= 1  # 0-based index
        school_id = s[chosen_id]
        max_power = school_max[school_id]
        if p[chosen_id] < max_power:
            needed += 1
            
    print(needed)

if __name__ == "__main__":
    solve()