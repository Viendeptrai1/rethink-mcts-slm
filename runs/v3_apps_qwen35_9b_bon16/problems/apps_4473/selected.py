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
        
        pairs = k // 2
        remainder = k % 2
        
        current_pos = pairs * (a - b)
        
        if remainder == 1:
            current_pos += a
            
        results.append(str(current_pos))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == "__main__":
    solve()