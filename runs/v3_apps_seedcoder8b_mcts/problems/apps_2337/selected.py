def minimum_additional_problems(n, m, required_complexities, prepared_complexities):
    # Sort the prepared complexities for easier comparison
    prepared_complexities.sort()
    
    # Initialize pointers and counters
    req_ptr = 0
    prep_ptr = 0
    additional_problems = 0
    
    # Iterate over the required complexities
    while req_ptr < n:
        # If there are prepared problems and the current prepared problem can meet the requirement
        if prep_ptr < m and prepared_complexities[prep_ptr] >= required_complexities[req_ptr]:
            prep_ptr += 1
        else:
            # If the current prepared problem cannot meet the requirement, we need to add a new problem
            additional_problems += 1
        req_ptr += 1
    
    return additional_problems

# Read input
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