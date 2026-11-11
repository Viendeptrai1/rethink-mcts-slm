from math import comb

def sum_of_max_values(N, K, a):
    MOD = 1000000007
    
    # Sort the array
    a.sort()
    
    total_sum = 0
    
    # Calculate the contribution of each element
    for i in range(N):
        # Number of elements greater than or equal to a[i]
        greater_equal_count = N - i
        
        # Number of ways to choose K-1 elements from these greater_equal_count
        if greater_equal_count >= K:
            ways_to_choose_greater_equal = comb(greater_equal_count - 1, K - 1)
        else:
            ways_to_choose_greater_equal = 0
        
        # Number of ways to choose the remaining K-ways_greater_equal elements from the smaller elements
        smaller_count = i
        ways_to_choose_smaller = comb(smaller_count, K - ways_to_choose_greater_equal)
        
        # Total ways to form a combination where a[i] is the maximum
        total_ways = ways_to_choose_greater_equal * ways_to_choose_smaller
        
        # Add the contribution of a[i] to the total sum
        total_sum = (total_sum + a[i] * total_ways) % MOD
    
    return total_sum

# Read input
N, K = map(int, input().split())
a = list(map(int, input().split()))

# Calculate and print the result
result = sum_of_max_values(N, K, a)
print(result)