import sys

def min_last_exam_day(n, exams):
    # Sort exams based on the scheduled date a_i
    exams.sort(key=lambda x: x[0])
    
    # Initialize the dp array where dp[i] represents the minimum last exam day
    # if we consider the first i+1 exams
    dp = [float('inf')] * n
    
    # Base case: the minimum last exam day for the first exam is either a_0 or b_0
    dp[0] = min(exams[0][0], exams[0][1])
    
    # Fill the dp array
    for i in range(1, n):
        a_i, b_i = exams[i]
        # Option 1: Take the i-th exam on day a_i
        dp[i] = max(dp[i-1], a_i)
        # Option 2: Take the i-th exam on day b_i if it doesn't violate the order
        if b_i >= dp[i-1]:
            dp[i] = min(dp[i], b_i)
    
    # The answer is the minimum last exam day for all exams
    return dp[-1]

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
exams = []
index = 1
for _ in range(n):
    a_i = int(data[index])
    b_i = int(data[index + 1])
    exams.append((a_i, b_i))
    index += 2

# Output the result
print(min_last_exam_day(n, exams))