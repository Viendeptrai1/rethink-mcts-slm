import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
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
    
    results = []
    for i in range(N):
        sx, sy = students[i]
        min_dist = float('inf')
        best_idx = -1
        
        for j in range(M):
            cx, cy = checkpoints[j]
            dist = abs(sx - cx) + abs(sy - cy)
            
            if dist < min_dist:
                min_dist = dist
                best_idx = j + 1  # 1-based index
        
        results.append(best_idx)
    
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()