def count_valid_multiples(X, A, B, allowed_digits):
    from itertools import product

    allowed_digits = set(allowed_digits)
    count = 0

    def is_valid_number(num_str):
        return all(d in allowed_digits for d in num_str)

    def generate_numbers_with_digits(digits, max_len):
        for length in range(1, max_len + 1):
            for num_tuple in product(digits, repeat=length):
                if num_tuple[0] == '0':
                    continue
                yield int(''.join(num_tuple))

    max_len = len(str(B))
    for number in generate_numbers_with_digits(allowed_digits, max_len):
        if A <= number <= B and number % X == 0:
            count += 1

    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    X = int(data[0])
    A = int(data[1])
    B = int(data[2])
    allowed_digits = data[3]
    result = count_valid_multiples(X, A, B, allowed_digits)
    print(result)