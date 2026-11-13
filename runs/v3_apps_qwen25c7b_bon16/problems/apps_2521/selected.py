import sys
from typing import List

def max_score(N: int, a: List[int]) -> int:
    # Calculate the prefix sums
    prefix_sum = [0] * (3 * N)
    for i in range(3 * N):
        prefix_sum[i] = prefix_sum[i - 1] + a[i]
    
    # Calculate the suffix sums
    suffix_sum = [0] * (3 * N)
    for i in range(3 * N - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + a[i]
    
    # Find the maximum score by removing N elements
    max_score = float('-inf')
    for i in range(N, 2 * N):
        left_sum = prefix_sum[i - 1]
        right_sum = suffix_sum[i + 1]
        current_score = left_sum - right_sum
        if current_score > max_score:
            max_score = current_score
    
    return max_score

# Main function to read input and print the result
if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    a = list(map(int, data[1:]))
    result = max_score(N, a)
    print(result)