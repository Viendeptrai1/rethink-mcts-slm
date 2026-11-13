def count_good_plans(n, m, b, mod, a):
    # Initialize a 2D DP array with dimensions (m+1) x (b+1)
    dp = [[0] * (b + 1) for _ in range(m + 1)]
    dp[0][0] = 1  # Base case: 1 way to write 0 lines with 0 bugs

    # Iterate over each programmer
    for i in range(n):
        # Create a temporary DP array for the current programmer
        new_dp = [[0] * (b + 1) for _ in range(m + 1)]
        bugs_per_line = a[i]

        # Iterate over each possible number of lines
        for lines in range(m + 1):
            # Iterate over each possible number of bugs
            for bugs in range(b + 1):
                if dp[lines][bugs] > 0:
                    # Try writing 0 to (m-lines) lines by the current programmer
                    for x in range(m - lines + 1):
                        new_bugs = bugs + x * bugs_per_line
                        if new_bugs <= b:
                            new_dp[lines + x][new_bugs] = (new_dp[lines + x][new_bugs] + dp[lines][bugs]) % mod

        # Update the main DP array with the new values
        dp = new_dp

    # Sum up all the ways to write exactly m lines with at most b bugs
    result = sum(dp[m][bugs] for bugs in range(b + 1)) % mod
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
b = int(data[2])
mod = int(data[3])
a = list(map(int, data[4:4 + n]))

# Output the result
print(count_good_plans(n, m, b, mod, a))