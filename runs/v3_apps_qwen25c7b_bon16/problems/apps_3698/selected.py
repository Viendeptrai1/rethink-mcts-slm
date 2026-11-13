def count_special_numbers(n, k):
    MOD = 10**9 + 7
    
    # Convert binary string to integer
    n = int(n, 2)
    
    def binomial_coefficient(n, k):
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result % MOD
    
    def count_special_numbers_recursive(x, k, memo):
        if (x, k) in memo:
            return memo[(x, k)]
        
        if k == 0:
            return 1
        
        count = 0
        while x > 0:
            if x & 1:
                count += count_special_numbers_recursive((x >> 1) & ((1 << (x.bit_length() - 1)) - 1), k - 1, memo)
            else:
                break
            x >>= 1
        
        memo[(x, k)] = count
        return count
    
    return count_special_numbers_recursive(n, k, {})

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = data[0]
k = int(data[1])
result = count_special_numbers(n, k)
print(result)