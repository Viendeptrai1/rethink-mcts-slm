import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]

    # dp[i][state] = minimum rest days up to day i (0-indexed)
    # state: 0 = rest, 1 = sport, 2 = contest
    # Initialize with a large number
    INF = 10**9
    dp = [[INF] * 3 for _ in range(n)]

    # Base case: day 0
    day0 = a[0]
    # Option 0: Rest
    dp[0][0] = 1
    # Option 1: Sport (if gym is open: day0 == 2 or day0 == 3)
    if day0 == 2 or day0 == 3:
        dp[0][1] = 0
    # Option 2: Contest (if contest is held: day0 == 1 or day0 == 3)
    if day0 == 1 or day0 == 3:
        dp[0][2] = 0

    # Iterate through remaining days
    for i in range(1, n):
        day = a[i]
        
        # Try all previous states
        for prev_state in range(3):
            if dp[i-1][prev_state] == INF:
                continue
            
            # Try current state
            for curr_state in range(3):
                # Check if current activity is allowed based on day type
                allowed = False
                if curr_state == 0:
                    allowed = True  # Rest is always allowed
                elif curr_state == 1:
                    if day == 2 or day == 3:
                        allowed = True
                elif curr_state == 2:
                    if day == 1 or day == 3:
                        allowed = True
                
                if not allowed:
                    continue
                
                # Check constraint: cannot do same activity on consecutive days
                if prev_state == curr_state and curr_state != 0:
                    continue
                
                # Update DP
                rest_cost = 1 if curr_state == 0 else 0
                dp[i][curr_state] = min(dp[i][curr_state], dp[i-1][prev_state] + rest_cost)

    # Answer is the minimum of the last day's states
    print(min(dp[n-1]))

if __name__ == "__main__":
    solve()