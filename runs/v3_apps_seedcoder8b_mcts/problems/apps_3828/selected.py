def min_moves_to_sort(n, p):
    from bisect import bisect_left

    # Function to find the length of the Longest Increasing Subsequence (LIS)
    def length_of_lis(sequence):
        lis = []
        for value in sequence:
            pos = bisect_left(lis, value)
            if pos == len(lis):
                lis.append(value)
            else:
                lis[pos] = value
        return len(lis)

    # Calculate the length of the LIS
    lis_length = length_of_lis(p)

    # The minimum number of moves is the total number of cars minus the length of the LIS
    return n - lis_length

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
p = list(map(int, data[1:n+1]))

# Output the result
print(min_moves_to_sort(n, p))