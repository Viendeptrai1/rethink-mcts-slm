import sys

# Increase recursion depth just in case, though iterative DP is preferred for very large states.
sys.setrecursionlimit(20000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    X = int(input_data[0])
    A = int(input_data[1])
    B = int(input_data[2])
    allowed_str = input_data[3]
    
    # Convert allowed digits to a set for O(1) lookup and a sorted list for iteration
    allowed_digits = set(allowed_str)
    allowed_list = sorted([int(d) for d in allowed_str])

    # Helper function to count valid multiples in range [1, N]
    def count_valid(N):
        if N < 1:
            return 0
        
        s = str(N)
        n_len = len(s)
        
        # Memoization table: (position, remainder, tight, started) -> count
        # We use a dictionary for sparse memoization since states might not be fully dense
        memo = {}

        def dp(pos, rem, tight, started):
            if pos == n_len:
                # If we have started (meaning we formed a non-zero number), check if it's a multiple
                if started and rem == 0:
                    return 1
                return 0
            
            state = (pos, rem, tight, started)
            if state in memo:
                return memo[state]
            
            limit = int(s[pos]) if tight else 9
            
            total = 0
            
            for d in allowed_list:
                # If tight constraint is active, we cannot pick a digit larger than limit
                if tight and d > limit:
                    continue
                
                new_tight = tight and (d == limit)
                
                if not started:
                    if d == 0:
                        # Continue with leading zeros, number not started yet
                        # Remainder stays 0, started stays False
                        total += dp(pos + 1, 0, new_tight, False)
                    else:
                        # Start the number
                        # New remainder is d % X
                        new_rem = d % X
                        total += dp(pos + 1, new_rem, new_tight, True)
                else:
                    # Number has already started
                    # Update remainder: (rem * 10 + d) % X
                    new_rem = (rem * 10 + d) % X
                    total += dp(pos + 1, new_rem, new_tight, True)
            
            memo[state] = total
            return total

        return dp(0, 0, True, False)

    # Result is count(B) - count(A-1)
    result = count_valid(B) - count_valid(A - 1)
    print(result)

if __name__ == "__main__":
    solve()