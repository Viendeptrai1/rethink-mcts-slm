import sys

def main():
    import sys
    import bisect
    
    def lis_with_moves(arr):
        n = len(arr)
        left = arr[:]
        right = arr[::-1]
        
        lis_left = [left[0]]
        moves_left = ['L']
        for i in range(1, n):
            if left[i] > lis_left[-1]:
                lis_left.append(left[i])
                moves_left.append('L')
            else:
                idx = bisect.bisect_left(lis_left, left[i])
                lis_left[idx] = left[i]
                moves_left[idx] = 'L'
        
        lis_right = [right[0]]
        moves_right = ['R']
        for i in range(1, n):
            if right[i] > lis_right[-1]:
                lis_right.append(right[i])
                moves_right.append('R')
            else:
                idx = bisect.bisect_left(lis_right, right[i])
                lis_right[idx] = right[i]
                moves_right[idx] = 'R'
        
        if len(lis_left) >= len(lis_right):
            return len(lis_left), ''.join(moves_left)
        else:
            return len(lis_right), ''.join(reversed(moves_right))
    
    n = int(sys.stdin.readline().strip())
    arr = list(map(int, sys.stdin.readline().strip().split()))
    
    k, s = lis_with_moves(arr)
    print(k)
    print(s)

if __name__ == "__main__":
    main()