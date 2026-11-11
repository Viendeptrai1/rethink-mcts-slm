import sys

def find_reversible_subsequence(n, values):
    # Find the first place where the sequence is not in non-decreasing order
    start = -1
    for i in range(n - 1):
        if values[i] > values[i + 1]:
            start = i
            break
    
    # If already sorted, return impossible
    if start == -1:
        return "impossible"
    
    # Find the last place where the sequence is not in non-decreasing order
    end = -1
    for i in range(n - 1, 0, -1):
        if values[i] < values[i - 1]:
            end = i
            break
    
    # Reverse the subsequence from start+1 to end
    reversed_values = values[:start + 1] + values[start + 1:end + 1][::-1] + values[end + 1:]
    
    # Check if the entire sequence is now sorted
    for i in range(n - 1):
        if reversed_values[i] > reversed_values[i + 1]:
            return "impossible"
    
    # Return 1-based indices
    return f"{start + 1} {end + 1}"

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
values = list(map(int, data[1:]))

# Find and print the result
result = find_reversible_subsequence(n, values)
print(result)