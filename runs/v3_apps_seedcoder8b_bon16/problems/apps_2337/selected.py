def minimum_additional_problems(n, m, required_complexities, prepared_complexities):
    import bisect

    # Sort the required complexities to use binary search for checking
    required_complexities.sort()

    # Count the number of prepared problems that meet the requirements
    used_problems = 0
    prepared_complexities.sort()

    for complexity in required_complexities:
        # Use binary search to find the first problem in prepared_complexities >= complexity
        idx = bisect.bisect_left(prepared_complexities, complexity)
        if idx < len(prepared_complexities):
            used_problems += 1
            prepared_complexities.pop(idx)  # Remove the problem to avoid reusing

    # The number of additional problems needed is the difference between
    # the number of required complexities and the number of used prepared problems
    additional_problems_needed = n - used_problems

    return additional_problems_needed

# Read input from standard input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
required_complexities = list(map(int, data[2:n+2]))
prepared_complexities = list(map(int, data[n+2:n+2+m]))

# Get the result and print it
result = minimum_additional_problems(n, m, required_complexities, prepared_complexities)
print(result)