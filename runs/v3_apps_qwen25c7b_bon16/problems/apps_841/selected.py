def generate_sequence(n):
    if n == 1:
        return "1337"
    
    # Calculate the number of '7's needed
    num_sevens = (n - 1) // 4
    
    # Calculate the number of '3's needed
    num_threes = (n - 1 - num_sevens * 4) // 2
    
    # Calculate the number of '1's needed
    num_ones = n - num_sevens - num_threes
    
    # Construct the sequence
    result = ["7"] * num_sevens + ["3"] * num_threes + ["1"] * num_ones
    return "".join(result)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    for i in range(1, t + 1):
        n = int(data[i])
        result = generate_sequence(n)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()