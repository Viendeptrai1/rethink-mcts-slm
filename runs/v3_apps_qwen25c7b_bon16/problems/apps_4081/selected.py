from sys import stdin, stdout

def solve():
    n = int(stdin.readline())
    a = list(map(int, stdin.readline().split()))
    
    # Create a mapping from value to its index
    index_map = {value: i for i, value in enumerate(a)}
    
    # Initialize variables to track the longest increasing subsequence
    max_length = 0
    moves = []
    
    # Use two pointers to find the longest increasing subsequence
    left = 0
    right = n - 1
    
    while left <= right:
        if a[left] == left + 1:
            moves.append('L')
            left += 1
        elif a[right] == right + 1:
            moves.append('R')
            right -= 1
        else:
            # Find the next larger element on the left side
            next_larger_left = None
            for i in range(left + 1, right + 1):
                if a[i] > a[left]:
                    next_larger_left = i
                    break
            
            # Find the next larger element on the right side
            next_larger_right = None
            for i in range(right - 1, left - 1, -1):
                if a[i] > a[right]:
                    next_larger_right = i
                    break
            
            if next_larger_left is not None and next_larger_right is not None:
                if index_map[a[next_larger_left]] < index_map[a[next_larger_right]]:
                    moves.append('L')
                    left = next_larger_left + 1
                else:
                    moves.append('R')
                    right = next_larger_right - 1
            elif next_larger_left is not None:
                moves.append('L')
                left = next_larger_left + 1
            else:
                moves.append('R')
                right = next_larger_right - 1
    
    # Output the result
    stdout.write(f"{len(moves)}\n")
    stdout.write("".join(moves) + "\n")

# Call the solve function
solve()