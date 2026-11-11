import sys

def find_reversible_subsequence(n, values):
    # Find the first place where the sequence is not in non-decreasing order
    start = -1
    for i in range(n - 1):
        if values[i] > values[i + 1]:
            start = i
            break
    
    # If the entire sequence is already sorted
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
    
    # Check if the reversed subsequence results in a sorted sequence
    for i in range(n - 1):
        if reversed_values[i] > reversed_values[i + 1]:
            return "impossible"
    
    # Return the 1-based indices of the subsequence
    return f"{start + 2} {end + 1}"

# Read input
n = int(sys.stdin.readline())
values = list(map(int, sys.stdin.readline().split()))

# Find and print the result
result = find_reversible_subsequence(n, values)
print(result)