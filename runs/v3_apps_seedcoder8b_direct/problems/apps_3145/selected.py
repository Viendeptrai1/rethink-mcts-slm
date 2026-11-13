def count_valid_multiples(X, A, B, allowed_digits):
    def is_valid_number(num_str):
        return all(char in allowed_digits for char in num_str)

    count = 0
    for multiple in range(A, B + 1):
        if multiple % X == 0:
            if is_valid_number(str(multiple)):
                count += 1
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    X = int(data[0])
    A = int(data[1])
    B = int(data[2])
    allowed_digits = data[3]
    
    result = count_valid_multiples(X, A, B, allowed_digits)
    print(result)

if __name__ == "__main__":
    main()