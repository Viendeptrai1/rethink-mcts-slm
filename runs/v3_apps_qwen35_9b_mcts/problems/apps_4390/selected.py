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
        
        remainder = a % b
        if remainder == 0:
            results.append(0)
        else:
            results.append(b - remainder)
    
    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()