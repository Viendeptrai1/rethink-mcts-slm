def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    left = 0
    right = n - 1
    result = []
    moves = []
    
    while left <= right:
        if a[left] < a[right]:
            if not result or a[left] > result[-1]:
                result.append(a[left])
                moves.append('L')
                left += 1
            else:
                result.append(a[right])
                moves.append('R')
                right -= 1
        elif a[left] > a[right]:
            if not result or a[right] > result[-1]:
                result.append(a[right])
                moves.append('R')
                right -= 1
            else:
                result.append(a[left])
                moves.append('L')
                left += 1
        else:
            if not result or a[left] > result[-1]:
                result.append(a[left])
                moves.append('L')
                left += 1
            else:
                result.append(a[right])
                moves.append('R')
                right -= 1
    
    print(len(result))
    print(''.join(moves))

if __name__ == "__main__":
    solve()