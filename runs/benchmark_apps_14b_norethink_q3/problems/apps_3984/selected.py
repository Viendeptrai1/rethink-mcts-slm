import sys

def determine_winner(s):
    n = len(s)
    dp = [None] * n
    
    def can_win(l, r):
        if dp[l] is not None:
            return dp[l]
        
        # Try to find a move for Ann
        for l_prime in range(l, -1, -1):
            for r_prime in range(r, n):
                if s[l_prime:r_prime+1] < s[l:r+1]:
                    if not can_win(l_prime, r_prime):
                        dp[l] = True
                        return True
        
        dp[l] = False
        return False
    
    results = []
    for k in range(n):
        if can_win(k, k):
            results.append("Ann")
        else:
            results.append("Mike")
    
    return results

def main():
    import sys
    s = sys.stdin.read().strip()
    results = determine_winner(s)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()