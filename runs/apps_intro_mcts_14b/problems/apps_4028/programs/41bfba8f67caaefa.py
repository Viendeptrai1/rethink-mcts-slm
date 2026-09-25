import sys

MOD = 10**9 + 7

def catalan(n):
    if n == 0:
        return 1
    res_num = 1
    res_den = 1
    for i in range(2, n + 1):
        res_num *= (n + i)
        res_den *= i
    return res_num // res_den

def count_valid_sequences(n, s):
    len_s = len(s)
    total_length = 2 * n
    if len_s > total_length:
        return 0
    
    # Precompute Catalan numbers
    catalan_numbers = [0] * (n + 1)
    for i in range(n + 1):
        catalan_numbers[i] = catalan(i)
    
    def is_valid_prefix(prefix):
        balance = 0
        for char in prefix:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return True
    
    def is_valid_suffix(suffix):
        balance = 0
        for char in reversed(suffix):
            if char == ')':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return True
    
    count = 0
    for start in range(total_length - len_s + 1):
        prefix = s[:start]
        suffix = s[start + len_s:]
        
        if is_valid_prefix(prefix) and is_valid_suffix(suffix):
            left_len = start
            right_len = total_length - len_s - start
            
            left_balance = 0
            for char in prefix:
                if char == '(':
                    left_balance += 1
                else:
                    left_balance -= 1
            
            right_balance = 0
            for char in suffix:
                if char == ')':
                    right_balance += 1
                else:
                    right_balance -= 1
            
            left_catalan = catalan_numbers[(left_len - left_balance) // 2]
            right_catalan = catalan_numbers[(right_len - right_balance) // 2]
            
            count = (count + left_catalan * right_catalan) % MOD
    
    return count

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