def min_problems_to_add(n, m, required_complexities, prepared_complexities):
    required_set = set(required_complexities)
    prepared_set = set(prepared_complexities)
    
    missing_count = 0
    
    for req in required_set:
        if req not in prepared_set:
            missing_count += 1
    
    return max(missing_count, n - len(prepared_set))

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

required_complexities = list(map(int, data[2:2+n]))
prepared_complexities = list(map(int, data[2+n:]))

# Output the result
print(min_problems_to_add(n, m, required_complexities, prepared_complexities))