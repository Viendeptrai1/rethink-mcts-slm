import sys

def main():
    import sys
    import bisect
    
    def lis_with_moves(arr):
        n = len(arr)
        if n == 0:
            return 0, ""
        
        # Initialize the list to store the smallest tail of all increasing subsequences
        # with different lengths
        lis = []
        # This will store the moves corresponding to the LIS
        moves = []
        
        for i in range(n):
            if not lis or arr[i] > lis[-1]:
                # If arr[i] is greater than the last element in lis, append it
                lis.append(arr[i])
                moves.append('L' if i == 0 else 'R')
            else:
                # Find the position to replace in lis
                pos = bisect.bisect_left(lis, arr[i])
                lis[pos] = arr[i]
                # Determine the move based on the position
                if pos == 0:
                    moves[pos] = 'L'
                else:
                    moves[pos] = 'R'
        
        # Reconstruct the moves string
        result_moves = []
        current_length = len(lis)
        for i in range(n - 1, -1, -1):
            if lis and arr[i] == lis[-1]:
                result_moves.append(moves[i])
                lis.pop()
        
        return current_length, ''.join(result_moves[::-1])
    
    # Read input
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    # Get the result
    k, s = lis_with_moves(a)
    
    # Print the result
    print(k)
    print(s)

if __name__ == "__main__":
    main()