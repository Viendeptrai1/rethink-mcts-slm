def solve(N):
    # Calculate the sum of the digits of N
    digit_sum = sum(int(digit) for digit in str(N))
    
    # Convert the sum to binary and return it as a string
    return bin(digit_sum)[2:]