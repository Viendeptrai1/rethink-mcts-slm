def count_integers(N, X, A):
    MOD = 998244353
    max_bits = X.bit_length()
    
    # Initialize a set to store all possible numbers
    possible_numbers = set()
    
    # Add initial numbers to the set
    for num in A:
        possible_numbers.add(num)
    
    # Process each number to generate new numbers
    for _ in range(max_bits):
        new_numbers = set()
        for num in possible_numbers:
            # Double the number
            doubled = num << 1
            if doubled <= X:
                new_numbers.add(doubled)
            
            # XOR with all other numbers
            for other in possible_numbers:
                xored = num ^ other
                if xored <= X:
                    new_numbers.add(xored)
        
        # Update the set of possible numbers
        possible_numbers.update(new_numbers)
    
    # Return the count of unique numbers modulo MOD
    return len(possible_numbers) % MOD

# Read input
N, X = map(int, input().split())
A = [int(input(), 2) for _ in range(N)]

# Call the function and print the result
result = count_integers(N, X, A)
print(result)