from math import sqrt

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def skjkasdkd(lst):
    max_prime = 0
    for num in lst:
        if is_prime(num) and num > max_prime:
            max_prime = num
    return sum(int(digit) for digit in str(max_prime))

# Test cases
print(skjkasdkd([0,3,2,1,3,5,7,4,5,5,5,2,181,32,4,32,3,2,32,324,4,3]))  # Output: 10
print(skjkasdkd([1,0,1,8,2,4597,2,1,3,40,1,2,1,2,4,2,5,1]))         # Output: 25
print(skjkasdkd([1,3,1,32,5107,34,83278,109,163,23,2323,32,30,1,9,3]))   # Output: 13
print(skjkasdkd([0,724,32,71,99,32,6,0,5,91,83,0,5,6]))               # Output: 11
print(skjkasdkd([0,81,12,3,1,21]))                                      # Output: 3
print(skjkasdkd([0,8,1,2,1,7]))                                          # Output: 7