def max_balanced_circle(n, heights):
    # Sort the heights to facilitate finding the longest balanced subsequence
    sorted_heights = sorted(heights)
    
    # Initialize variables to track the maximum length and the corresponding subsequence
    max_length = 0
    best_subseq = []
    
    # Iterate through each unique height
    for i in range(len(sorted_heights)):
        current_length = 1
        current_subseq = [sorted_heights[i]]
        
        # Check the next heights to form the longest balanced subsequence
        for j in range(i + 1, len(sorted_heights)):
            if abs(sorted_heights[j] - sorted_heights[j - 1]) <= 1:
                current_length += 1
                current_subseq.append(sorted_heights[j])
            else:
                break
        
        # Update the maximum length and the best subsequence found
        if current_length > max_length:
            max_length = current_length
            best_subseq = current_subseq
    
    # Return the result
    return max_length, best_subseq

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
heights = list(map(int, data[1:]))

# Get the result
result_length, result_subseq = max_balanced_circle(n, heights)

# Print the result
print(result_length)
print(" ".join(map(str, result_subseq)))