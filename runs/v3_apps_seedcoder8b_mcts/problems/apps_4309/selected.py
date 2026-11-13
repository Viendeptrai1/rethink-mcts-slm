def find_earliest_abc(n):
    n_str = str(n)
    first_digit = int(n_str[0])
    
    # Generate the smallest number with all same digits greater than or equal to n
    while True:
        candidate = str(first_digit) * len(n_str)
        if int(candidate) >= n:
            return candidate
        first_digit += 1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    N = int(input().strip())
    print(find_earliest_abc(N))