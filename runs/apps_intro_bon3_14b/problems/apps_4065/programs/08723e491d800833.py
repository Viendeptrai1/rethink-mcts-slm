import sys

def max_problems_in_contest(n, difficulties):
    # Initialize variables
    max_problems = 0
    current_end = -1
    
    # Iterate over each problem
    for i in range(n):
        # Find the farthest problem that satisfies the condition
        while current_end + 1 < n and difficulties[current_end + 1] <= difficulties[i] * 2:
            current_end += 1
        
        # Update the maximum number of problems
        max_problems = max(max_problems, current_end - i + 1)
    
    return max_problems

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
difficulties = list(map(int, data[1:]))

# Calculate and print the result
result = max_problems_in_contest(n, difficulties)
print(result)