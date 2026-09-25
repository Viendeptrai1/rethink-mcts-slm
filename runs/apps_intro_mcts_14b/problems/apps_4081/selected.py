import sys

def main():
    import sys
    import bisect
    
    def read_input():
        import sys
        return sys.stdin.read().split()
    
    data = read_input()
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    # Initialize variables
    left = 0
    right = n - 1
    lis = []
    path = []
    
    while left <= right:
        if a[left] < a[right]:
            if not lis or a[left] > lis[-1]:
                lis.append(a[left])
                path.append('L')
                left += 1
            else:
                idx = bisect.bisect_right(lis, a[left])
                lis[idx] = a[left]
                path[idx] = 'L'
                left += 1
        else:
            if not lis or a[right] > lis[-1]:
                lis.append(a[right])
                path.append('R')
                right -= 1
            else:
                idx = bisect.bisect_right(lis, a[right])
                lis[idx] = a[right]
                path[idx] = 'R'
                right -= 1
    
    # Output the result
    print(len(lis))
    print(''.join(path[:len(lis)]))

if __name__ == "__main__":
    main()