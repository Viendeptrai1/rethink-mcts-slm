def count_valid_multiples():
    import sys
    input = sys.stdin.read
    
    data = input().strip().split()
    X = int(data[0])
    A = int(data[1])
    B = int(data[2])
    allowed_digits = set(data[3])
    
    def is_valid_number(n):
        for digit in str(n):
            if digit not in allowed_digits:
                return False
        return True
    
    count = 0
    
    for multiple in range(X, B + 1, X):
        if multiple >= A and is_valid_number(multiple):
            count += 1
    
    print(count)

# Call the function
count_valid_multiples()