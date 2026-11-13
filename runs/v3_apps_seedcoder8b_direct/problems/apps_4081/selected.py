def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    # Initialize pointers for the left and right ends of the sequence
    left = 0
    right = n - 1
    
    # Initialize the result sequence and the move list
    result = []
    moves = []
    
    # Initialize the last added number to zero
    last_added = 0
    
    # While there are elements to consider
    while left <= right:
        # Check the leftmost and rightmost elements
        if a[left] > last_added and a[right] > last_added:
            # Choose the smaller of the two
            if a[left] < a[right]:
                result.append(a[left])
                moves.append('L')
                last_added = a[left]
                left += 1
            else:
                result.append(a[right])
                moves.append('R')
                last_added = a[right]
                right -= 1
        elif a[left] > last_added:
            # Only the leftmost element is valid
            result.append(a[left])
            moves.append('L')
            last_added = a[left]
            left += 1
        elif a[right] > last_added:
            # Only the rightmost element is valid
            result.append(a[right])
            moves.append('R')
            last_added = a[right]
            right -= 1
        else:
            # No more elements can be added
            break
    
    # Output the result
    print(len(result))
    print(''.join(moves))