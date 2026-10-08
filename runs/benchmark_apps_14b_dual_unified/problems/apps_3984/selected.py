import sys

def determine_winner(s):
    n = len(s)
    dp = [None] * n
    
    # Function to check if a substring is lexicographically smaller
    def is_smaller(l, r, l_prime, r_prime):
        return s[l_prime:r_prime+1] < s[l:r+1]
    
    # Initialize the dp array
    for k in range(n):
        dp[k] = 'Ann'  # Assume Ann wins initially
    
    # Fill the dp array
    for k in range(n):
        l, r = k, k
        while True:
            found = False
            for l_prime in range(l, -1, -1):
                for r_prime in range(r, n):
                    if is_smaller(l, r, l_prime, r_prime):
                        l, r = l_prime, r_prime
                        found = True
                        break
                if found:
                    break
            if not found:
                dp[k] = 'Mike'
                break
    
    return dp

def main():
    import sys
    s = sys.stdin.read().strip()
    result = determine_winner(s)
    for winner in result:
        print(winner)

if __name__ == "__main__":
    main()