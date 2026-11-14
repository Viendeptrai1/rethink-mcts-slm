import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        x1 = int(next(iterator))
        y1 = int(next(iterator))
        x2 = int(next(iterator))
        y2 = int(next(iterator))
        
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            results.append(1)
        elif dx == 0 or dy == 0:
            results.append(1)
        else:
            # The number of different sums is dx * dy + 1
            ans = dx * dy + 1
            results.append(ans)
            
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()