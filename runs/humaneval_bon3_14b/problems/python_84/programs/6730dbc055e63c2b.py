def solve(N):
    # Calculate the sum of the digits of N
    digit_sum = sum(int(digit) for digit in str(N))
    
    # Convert the sum to binary and return it as a string
    return bin(digit_sum)[2:]

# Example usage:
# print(solve(1000))  # Output: "1"
# print(solve(150))   # Output: "110"
# print(solve(147))   # Output: "1100"