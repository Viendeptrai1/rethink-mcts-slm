import sys

def find_reversible_subsequence(n, v):
    # Find the first place where the sequence is not in non-decreasing order
    start = -1
    for i in range(n - 1):
        if v[i] > v[i + 1]:
            start = i
            break
    
    # If the entire sequence is already sorted
    if start == -1:
        return "impossible"
    
    # Find the last place where the sequence is not in non-decreasing order
    end = -1
    for i in range(n - 1, 0, -1):
        if v[i] < v[i - 1]:
            end = i
            break
    
    # Reverse the subsequence from start+1 to end
    v_reversed = v[:start + 1] + v[start + 1:end + 1][::-1] + v[end + 1:]
    
    # Check if the entire sequence is now sorted
    for i in range(n - 1):
        if v_reversed[i] > v_reversed[i + 1]:
            return "impossible"
    
    # Return 1-based indices
    return f"{start + 1} {end + 1}"

# Read input
n = int(sys.stdin.readline())
v = list(map(int, sys.stdin.readline().split()))

# Find and print the result
result = find_reversible_subsequence(n, v)
print(result)