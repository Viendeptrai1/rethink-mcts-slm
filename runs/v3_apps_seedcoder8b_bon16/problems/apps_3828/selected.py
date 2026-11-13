def min_moves_to_sort(n, p):
    # Calculate the number of moves by finding the longest increasing subsequence (LIS)
    # that David Blaine can keep in place. The rest will need to be moved.
    
    # Helper function to calculate the LIS using binary search
    def calculate_lis(arr):
        import bisect
        lis = []
        for x in arr:
            pos = bisect.bisect_left(lis, x)
            if pos == len(lis):
                lis.append(x)
            else:
                lis[pos] = x
        return len(lis)
    
    # Calculate the longest increasing subsequence
    longest_increasing_subsequence_length = calculate_lis(p)
    
    # Minimum moves is total cars minus the length of LIS
    return n - longest_increasing_subsequence_length

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = list(map(int, data[1:n+1]))

# Get result and print
result = min_moves_to_sort(n, p)
print(result)