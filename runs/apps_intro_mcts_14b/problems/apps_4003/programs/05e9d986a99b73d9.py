import sys

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    left = 0
    right = n - 1
    result = []
    
    while left <= right:
        if a[left] < a[right]:
            result.append('L')
            left += 1
        else:
            result.append('R')
            right -= 1
    
    k = len(result)
    s = ''.join(result)
    
    print(k)
    print(s)

if __name__ == "__main__":
    solve()