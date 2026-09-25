import sys

def main():
    import sys
    import bisect
    
    def solve(n, a):
        # Initialize variables
        left = 0
        right = n - 1
        increasing_sequence = []
        moves = []
        
        while left <= right:
            if a[left] < a[right]:
                if not increasing_sequence or a[left] > increasing_sequence[-1]:
                    increasing_sequence.append(a[left])
                    moves.append('L')
                    left += 1
                else:
                    if a[right] > increasing_sequence[-1]:
                        increasing_sequence.append(a[right])
                        moves.append('R')
                        right -= 1
                    else:
                        left += 1
            else:
                if not increasing_sequence or a[right] > increasing_sequence[-1]:
                    increasing_sequence.append(a[right])
                    moves.append('R')
                    right -= 1
                else:
                    if a[left] > increasing_sequence[-1]:
                        increasing_sequence.append(a[left])
                        moves.append('L')
                        left += 1
                    else:
                        right -= 1
        
        return len(increasing_sequence), ''.join(moves)
    
    # Read input
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    # Solve the problem
    k, s = solve(n, a)
    
    # Print the result
    print(k)
    print(s)

if __name__ == "__main__":
    main()