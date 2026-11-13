import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        
        students = []
        for _ in range(N):
            a = int(next(iterator))
            b = int(next(iterator))
            students.append((a, b))
            
        checkpoints = []
        for _ in range(M):
            c = int(next(iterator))
            d = int(next(iterator))
            checkpoints.append((c, d))
            
    except StopIteration:
        return

    results = []
    
    for (sa, sb) in students:
        min_dist = float('inf')
        chosen_idx = -1
        
        for idx, (ca, cb) in enumerate(checkpoints):
            dist = abs(sa - ca) + abs(sb - cb)
            if dist < min_dist:
                min_dist = dist
                chosen_idx = idx + 1
        
        results.append(str(chosen_idx))
    
    print('\n'.join(results))

if __name__ == '__main__':
    solve()