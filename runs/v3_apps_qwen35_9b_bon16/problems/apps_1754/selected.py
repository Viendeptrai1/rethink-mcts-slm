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
        
    chosen = []
    for _ in range(k):
        chosen.append(int(next(iterator)) - 1)
        
    school_max = [0] * (m + 1)
    for i in range(n):
        school_id = s[i]
        power = p[i]
        if power > school_max[school_id]:
            school_max[school_id] = power
            
    needed = 0
    for cid in chosen:
        student_power = p[cid]
        school_id = s[cid]
        if student_power < school_max[school_id]:
            needed += 1
            
    print(needed)

if __name__ == "__main__":
    solve()