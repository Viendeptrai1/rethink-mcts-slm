def n_bit_color_code_with_palette():
    import sys
    from itertools import product
    
    # Read input
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    p = int(data[1])
    palette = set(map(int, data[2:2 + p]))
    
    # Generate all possible n-bit binary strings
    binary_strings = [''.join(p) for p in product('01', repeat=n)]
    
    # Function to calculate Hamming distance between two binary strings
    def hamming_distance(s1, s2):
        return sum(1 for x, y in zip(s1, s2) if x != y)
    
    # Function to backtrack and find a valid n-bit color code
    def backtrack(current_code):
        if len(current_code) == len(binary_strings):
            # Check if the last code to the first code also satisfies the palette
            if hamming_distance(current_code[0], current_code[-1]) in palette:
                return current_code
            return None
        
        last_string = current_code[-1]
        for string in binary_strings:
            if string not in current_code and hamming_distance(last_string, string) in palette:
                result = backtrack(current_code + [string])
                if result is not None:
                    return result
        return None
    
    # Try to generate a valid color code starting from each binary string
    for start_string in binary_strings:
        result = backtrack([start_string])
        if result is not None:
            for code in result:
                print(code)
            return
    
    # If no valid code was found, print "impossible"
    print("impossible")

# Execute the function
n_bit_color_code_with_palette()