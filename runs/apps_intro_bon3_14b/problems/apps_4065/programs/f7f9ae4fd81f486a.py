import sys

def max_contest_problems(n, difficulties):
    # Initialize variables
    max_problems = 0
    current_end = -1
    
    # Iterate over each problem
    for i in range(n):
        # Check if the current problem can be included in the contest
        if difficulties[i] <= 2 * current_end:
            continue
        
        # Update the end of the current contest
        current_end = difficulties[i]
        max_problems += 1
    
    return max_problems

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
difficulties = list(map(int, data[1:]))

# Calculate and print the result
result = max_contest_problems(n, difficulties)
print(result)