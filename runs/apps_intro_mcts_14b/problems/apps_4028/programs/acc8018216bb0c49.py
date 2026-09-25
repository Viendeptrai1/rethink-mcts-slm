import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_valid_sequences(n, s):
    def catalan_number(k):
        if k == 0 or k == 1:
            return 1
        catalan = [0] * (k + 1)
        catalan[0] = 1
        catalan[1] = 1
        for i in range(2, k + 1):
            for j in range(i):
                catalan[i] = (catalan[i] + catalan[j] * catalan[i - j - 1]) % MOD
        return catalan[k]

    def is_valid_bracket_sequence(seq):
        balance = 0
        for char in seq:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    if not is_valid_bracket_sequence(s):
        return 0

    n_s = len(s)
    if n_s > 2 * n:
        return 0

    # Calculate the number of ways to place s in a sequence of length 2n
    left_length = n - (n_s // 2)
    right_length = n - (n_s - n_s // 2)

    if left_length < 0 or right_length < 0:
        return 0

    left_catalan = catalan_number(left_length)
    right_catalan = catalan_number(right_length)

    result = (left_catalan * right_catalan) % MOD
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = count_valid_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()