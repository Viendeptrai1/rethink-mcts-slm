import sys

def main():
    import sys
    import bisect
    
    def solve(n, a):
        # Initialize the DP table
        dp = []
        path = []
        
        left = 0
        right = n - 1
        
        while left <= right:
            if a[left] < a[right]:
                if not dp or a[left] > dp[-1]:
                    dp.append(a[left])
                    path.append('L')
                    left += 1
                else:
                    idx = bisect.bisect_right(dp, a[right])
                    if idx < len(dp):
                        dp[idx] = a[right]
                        path[idx] = 'R'
                    right -= 1
            else:
                if not dp or a[right] > dp[-1]:
                    dp.append(a[right])
                    path.append('R')
                    right -= 1
                else:
                    idx = bisect.bisect_right(dp, a[left])
                    if idx < len(dp):
                        dp[idx] = a[left]
                        path[idx] = 'L'
                    left += 1
        
        return len(dp), ''.join(path)
    
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