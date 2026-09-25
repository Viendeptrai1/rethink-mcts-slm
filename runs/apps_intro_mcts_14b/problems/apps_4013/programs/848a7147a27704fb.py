import sys
from typing import List

def min_instability(n: int, a: List[int]) -> int:
    a.sort()
    min_instab = float('inf')
    
    # Calculate instability by removing each element one by one
    for i in range(n):
        if i == 0:
            instab = a[-1] - a[1]
        elif i == n - 1:
            instab = a[-2] - a[0]
        else:
            instab = max(a[i-1], a[-1]) - min(a[0], a[i+1])
        
        min_instab = min(min_instab, instab)
    
    return min_instab

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = min_instability(n, a)
    print(result)

if __name__ == "__main__":
    main()