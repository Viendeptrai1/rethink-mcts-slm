import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    for _ in range(t):
        a = int(next(iterator))
        b = int(next(iterator))
        k = int(next(iterator))
        
        full_pairs = k // 2
        remainder = k % 2
        
        # Each pair (right a, left b) results in net change of (a - b)
        position = full_pairs * (a - b)
        
        # If there is an odd jump left, it's always a right jump of size a
        if remainder == 1:
            position += a
            
        results.append(str(position))
    
    print('\n'.join(results))

if __name__ == "__main__":
    solve()