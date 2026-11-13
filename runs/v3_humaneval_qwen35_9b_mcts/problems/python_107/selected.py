def even_odd_palindrome(n):
    even_count = 0
    odd_count = 0
    
    # Single-digit palindromes: 1 to 9
    for i in range(1, 10):
        if i <= n:
            if i % 2 == 0:
                even_count += 1
            else:
                odd_count += 1
    
    # Two-digit palindromes: 11, 22, ..., 99
    for i in range(1, 10):
        palindrome = i * 11
        if palindrome <= n:
            if palindrome % 2 == 0:
                even_count += 1
            else:
                odd_count += 1
    
    # Three-digit palindromes: 101, 111, ..., 999
    # Form: aba where a in 1..9, b in 0..9
    for a in range(1, 10):
        for b in range(10):
            palindrome = a * 100 + b * 10 + a
            if palindrome <= n:
                if palindrome % 2 == 0:
                    even_count += 1
                else:
                    odd_count += 1
            else:
                # Since palindromes increase with b, we can break early if needed
                # but given n <= 1000, simple break is sufficient
                break
    
    return (even_count, odd_count)