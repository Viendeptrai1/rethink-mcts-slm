import sys

def find_sequence(n):
    if n == 1:
        return "1337"
    
    # We need to construct a sequence with exactly n subsequences of "1337"
    # The sequence will be in the form of "1" followed by "3" repeated k times, then "7" repeated m times
    # The number of subsequences "1337" in this sequence is (k+1)*(m+1)
    # We need to find k and m such that (k+1)*(m+1) = n
    
    # Start with k = 0 and find the corresponding m
    k = 0
    while (k + 1) * (n // (k + 1)) != n:
        k += 1
    
    m = n // (k + 1) - 1
    
    # Construct the sequence
    sequence = "1" + "3" * k + "7" * m
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