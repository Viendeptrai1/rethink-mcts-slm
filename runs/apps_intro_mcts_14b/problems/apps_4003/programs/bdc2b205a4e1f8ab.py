import sys

def main():
    import sys
    import sys
    import sys
    
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    
    left = 0
    right = n - 1
    result = []
    
    while left <= right:
        if a[left] < a[right]:
            if not result or a[left] > result[-1]:
                result.append(a[left])
                left += 1
            else:
                if a[right] > result[-1]:
                    result.append(a[right])
                    right -= 1
                else:
                    left += 1
        else:
            if not result or a[right] > result[-1]:
                result.append(a[right])
                right -= 1
            else:
                if a[left] > result[-1]:
                    result.append(a[left])
                    left += 1
                else:
                    right -= 1
    
    k = len(result)
    moves = []
    
    left = 0
    right = n - 1
    i = 0
    
    while left <= right:
        if a[left] < a[right]:
            if i < k and a[left] == result[i]:
                moves.append('L')
                left += 1
                i += 1
            else:
                moves.append('R')
                right -= 1
        else:
            if i < k and a[right] == result[i]:
                moves.append('R')
                right -= 1
                i += 1
            else:
                moves.append('L')
                left += 1
    
    print(k)
    print(''.join(moves))

if __name__ == "__main__":
    main()