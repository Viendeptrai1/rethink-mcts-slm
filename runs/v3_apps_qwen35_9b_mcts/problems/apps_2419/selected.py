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
        
        diff = abs(a - b)
        
        if diff == 0:
            results.append(0)
            continue
        
        k = 0
        total = 0
        while total < diff:
            k += 1
            total += k
        
        remainder = total - diff
        
        if remainder % 2 == 0:
            results.append(k)
        else:
            results.append(k + 1)
    
    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()