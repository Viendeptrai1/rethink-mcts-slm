import sys

def find_sequence(n):
    if n == 1:
        return "1337"
    
    # We need to construct a sequence with exactly n subsequences of "1337"
    # The sequence will be of the form "1337" followed by some number of "1"s
    # Each "1" added after "1337" will double the number of subsequences
    num_ones = 0
    while (1 << num_ones) < n:
        num_ones += 1
    
    # If (1 << num_ones) is greater than n, we need to adjust
    if (1 << num_ones) > n:
        num_ones -= 1
    
    # Now we need to add the remaining ones to reach exactly n subsequences
    remaining = n - (1 << num_ones)
    
    # The sequence will be "1337" followed by num_ones "1"s and then remaining "1"s
    sequence = "1337" + "1" * num_ones + "1" * remaining
    
    return sequence

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        n = int(data[index])
        results.append(find_sequence(n))
        index += 1
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()