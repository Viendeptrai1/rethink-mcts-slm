def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary.
    
    Example
        For N = 1000, the sum of digits will be 1 the output should be "1".
        For N = 150, the sum of digits will be 6 the output should be "110".
        For N = 147, the sum of digits will be 12 the output should be "1100".
    
    Variables:
        @N integer
             Constraints: 0 ≤ N ≤ 10000.
    Output:
         a string of binary number
    """
    if N < 0:
        raise ValueError("N must be a non-negative integer")
    
    digit_sum = sum(int(digit) for digit in str(N))
    
    if digit_sum == 0:
        return "0"
    
    binary_representation = bin(digit_sum)[2:]
    
    return binary_representation