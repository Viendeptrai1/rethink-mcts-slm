import sys
from typing import List

def min_instability(n: int, a: List[int]) -> int:
    a.sort()
    min_instab = float('inf')
    
    for i in range(n):
        instab = max(a[i+1] - a[0], a[n-1] - a[i])
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